from collections import OrderedDict

from django.contrib.auth import get_user_model
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.request import Request
from rest_framework.serializers import (ListField, ModelSerializer,
                                        SerializerMethodField,
                                        SlugRelatedField)

from common.constants import PATIENT
from common.utils import (create_nested_objects, extract_fields,
                          remove_blank_or_null)
from medicines.models import MedicineBrand
from organizations.models import Organization, OrganizationHasUserWithRole

from .models import (FeedbackToOrganization, MessageBetweenUserOrganization,
                     Prescription, PrescriptionFeedback,
                     PrescriptionHasMedicine, PrescriptionMessage)


class FeedbackSerializer(ModelSerializer):
    class Meta:
        model = FeedbackToOrganization
        fields = (
            "uuid",
            "user",
            "organization",
            "content",
            "rating",
        )
        read_only_fields = (
            "uuid",
            "user",
            "organization",
        )

    user = SlugRelatedField(slug_field="uuid", read_only=True)
    organization = SlugRelatedField(slug_field="uuid", read_only=True)

    def create(self, validated_data):
        request: Request = self.context.get("request")
        auth_user: get_user_model() = request.user
        view = self.context.get("view")
        organization = view.kwarg_objects.get("org_uuid")
        add_data = {
            "organization": organization,
            "user": auth_user,
        }
        validated_data.update(add_data)
        return super().create(validated_data)


class MessageSerializer(ModelSerializer):
    class Meta:
        model = MessageBetweenUserOrganization
        fields = ("uuid", "user", "organization", "content", "from_user")
        read_only_fields = ("uuid", "user", "organization", "from_user")

    user = SlugRelatedField(slug_field="uuid", read_only=True)
    organization = SlugRelatedField(slug_field="uuid", read_only=True)

    def create(self, validated_data):
        request: Request = self.context.get("request")
        auth_user: get_user_model() = request.user
        view = self.context.get("view")
        recepient = view.kwarg_objects.get("user_uuid")
        organization = view.kwarg_objects.get("org_uuid")
        from_user = False if recepient else True
        new_data = {
            "organization": organization,
            "user": recepient if recepient else auth_user,
            "from_user": from_user,
        }
        validated_data.update(new_data)
        return super().create(validated_data)


class PrescriptionHasMedicineSerializer(ModelSerializer):
    class Meta:
        model = PrescriptionHasMedicine
        fields = (
            "prescription",
            "brand",
            "instructions",
        )
        extra_kwargs = {"prescription": {"write_only": True, "required": False}}

    brand = SlugRelatedField(queryset=MedicineBrand.objects.filter(), slug_field="slug")

    def is_valid(self, *, raise_exception=False):
        self.initial_data = remove_blank_or_null(self.initial_data)
        return super().is_valid(raise_exception=raise_exception)


class PrescriptionSerializer(ModelSerializer):
    class Meta:
        model = Prescription
        fields = (
            "uuid",
            "organization",
            "doctor",
            "patient",
            "prescribed_medicines_write_only",
            "prescribed_medicines",
            "done",
        )
        read_only_fields = (
            "uuid",
            "organization",
            "doctor",
        )

    organization = SlugRelatedField(slug_field="uuid", read_only=True)
    doctor = SlugRelatedField(slug_field="uuid", read_only=True)
    patient = SlugRelatedField(
        queryset=get_user_model().objects.filter(), slug_field="uuid"
    )
    prescribed_medicines_write_only = ListField(allow_empty=False, write_only=True)
    # prescribed_medicines = PrescriptionHasMedicineSerializer(many=True)
    prescribed_medicines = SerializerMethodField(read_only=True)

    def get_prescribed_medicines(self, obj):  # Need FIX
        if type(obj) is not OrderedDict:
            prescribed_medicines = PrescriptionHasMedicine.objects.filter(
                prescription_id=obj.id
            )
            serializer = PrescriptionHasMedicineSerializer(
                prescribed_medicines, many=True
            )
            return serializer.data

    def is_valid(self, *, raise_exception=False):
        self.initial_data = remove_blank_or_null(self.initial_data)
        return super().is_valid(raise_exception=raise_exception)

    def validate_patient(self, obj):
        patient_uuid = obj.uuid
        request = self.context.get("request")
        org_uuid = request.parser_context.get("kwargs").get("org_uuid")
        try:
            relation = OrganizationHasUserWithRole.objects.select_related().get(
                organization__uuid=org_uuid, user__uuid=patient_uuid
            )
        except OrganizationHasUserWithRole.DoesNotExist:
            raise NotFound({"patient": "User not found."})

        if relation.role == PATIENT:
            return obj
        else:
            raise ValidationError({"patient": "User is not patient in organization."})

    def validate_prescribed_medicines_write_only(self, data):
        prescribed_medicines = data[0]
        request = self.context.get("request")
        org_uuid = request.parser_context.get("kwargs").get("org_uuid")
        for prescribed_medicine in prescribed_medicines:
            try:
                brand = MedicineBrand.objects.get(slug=prescribed_medicine.get("brand"))
                if brand.manufacturer.uuid != org_uuid:
                    raise ValidationError(
                        f"{brand.name} is not manufactured by organization."
                    )
            except MedicineBrand.DoesNotExist:
                raise ValidationError("Medicine not found")
        return data

    def create(self, validated_data):
        to_exclude = ("prescribed_medicines_write_only",)
        validated_data, extracted_data = extract_fields(
            data=validated_data, fields=to_exclude
        )
        request = self.context.get("request")
        org_uuid = request.parser_context.get("kwargs").get("org_uuid")
        organization = Organization.objects.get(uuid=org_uuid)
        add_data = {"organization": organization, "doctor": request.user}
        validated_data.update(add_data)
        instance = super().create(validated_data)

        # Following code snippet needs checking and refactoring for a better solution
        prescribed_medicines = extracted_data.get("prescribed_medicines_write_only")[0]
        prescribed_medicines = [
            dict(prescribed_medicine) for prescribed_medicine in prescribed_medicines
        ]
        add_data = {"prescription": instance.id}

        for prescribed_medicine in prescribed_medicines:
            prescribed_medicine.update(add_data)
        ##############################################################################

        add_data = {"prescribed_medicines": prescribed_medicines}
        nested_fields = ("prescribed_medicines",)
        serializer_classes = (PrescriptionHasMedicineSerializer,)
        create_nested_objects(
            data=add_data,
            fields=nested_fields,
            serializer_classes=serializer_classes,
        )
        return instance


class PrescriptionFeedbackSerializer(ModelSerializer):
    class Meta:
        model = PrescriptionFeedback
        fields = (
            "uuid",
            "prescription",
            "user",
            "from_doctor",
            "content",
            "rating",
        )
        read_only_fields = (
            "uuid",
            "prescription",
            "user",
            "from_doctor",
        )

    prescription = SlugRelatedField(slug_field="uuid", read_only=True)
    user = SlugRelatedField(slug_field="uuid", read_only=True)

    def is_valid(self, *, raise_exception=False):
        self.initial_data = remove_blank_or_null(self.initial_data)
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        request: Request = self.context.get("request")
        auth_user: get_user_model() = request.user
        view = self.context.get("view")
        prescription = view.kwarg_objects.get("presc_uuid")
        org_uuid = view.kwargs.get("org_uuid")
        from_doctor = org_uuid is not None
        add_data = {
            "prescription": prescription,
            "user": auth_user,
            "from_doctor": from_doctor,
        }
        validated_data.update(add_data)
        return super().create(validated_data)


class PrescriptionMessageSerializer(PrescriptionFeedbackSerializer):
    class Meta:
        model = PrescriptionMessage
        fields = (
            "uuid",
            "prescription",
            "user",
            "from_doctor",
            "content",
        )
        read_only_fields = (
            "uuid",
            "prescription",
            "user",
            "from_doctor",
        )


class PrescriptionDetailSerializer(ModelSerializer):
    class Meta:
        model = Prescription
        fields = (
            "uuid",
            "organization",
            "doctor",
            "patient",
            "prescribed_medicines",
            "feedbacks",
            "chat",
            "done",
        )
        read_only_fields = (
            "uuid",
            "organization",
            "doctor",
            "patient",
            "prescribed_medicines",
            "feedbacks",
            "chat",
            "done",
        )

    organization = SlugRelatedField(slug_field="uuid", read_only=True)
    doctor = SlugRelatedField(slug_field="uuid", read_only=True)
    patient = SlugRelatedField(slug_field="uuid", read_only=True)
    prescribed_medicines = SerializerMethodField(read_only=True)
    feedbacks = SerializerMethodField(read_only=True)
    chat = SerializerMethodField(read_only=True)

    def get_prescribed_medicines(self, obj):  # Need FIX
        if type(obj) is not OrderedDict:
            prescribed_medicines = PrescriptionHasMedicine.objects.filter(
                prescription_id=obj.id
            )
            serializer = PrescriptionHasMedicineSerializer(
                prescribed_medicines, many=True
            )
            return serializer.data

    def get_feedbacks(self, obj):
        if type(obj) is not OrderedDict:
            request = self.context.get("request")
            auth_user = request.user
            feedbacks = (
                PrescriptionFeedback.objects.filter(prescription_id=obj.id)
                .exclude(user_id=auth_user.id)
                .order_by("-created_at")[:1]
            )
            serializer = PrescriptionFeedbackSerializer(feedbacks, many=True)
            return serializer.data

    def get_chat(self, obj):
        if type(obj) is not OrderedDict:
            request = self.context.get("request")
            auth_user = request.user
            chat = PrescriptionMessage.objects.filter(
                prescription_id=obj.id, user_id=auth_user.id
            ).order_by("-created_at")[:5]
            serializer = PrescriptionMessageSerializer(chat, many=True)
            return serializer.data
