from ..models.config import user_has_all_access


def is_form_relevant_to_user(user, action_model):
    for g in user.groups.all():
        if action_model.objects.filter(current_group=g).exists():
            return True
    return False


def get_assigned_forms(user, form_model):
    queryset = form_model.objects.exclude(
        status__is_draft=True).exclude(status__is_to_be_deleted=True)
    if user.is_authenticated and user_has_all_access(user):
        return queryset.exclude(
            assigned_to_group__permissions__codename='validator')
    else:
        return queryset.filter(assigned_to_group__in=user.groups.all())


def get_metadata_from_forms(forms):
    zones = forms.prefetch_related("redactors__team__zone") \
        .exclude(redactors__team__isnull=True) \
        .exclude(redactors__team__zone__isnull=True)\
        .values_list("redactors__team__zone__short_name", flat=True)
    statuses = forms.prefetch_related("status") \
        .exclude(status__isnull=True) \
        .values_list("status__label", flat=True)
    groups = forms.prefetch_related("assigned_to_group") \
        .exclude(assigned_to_group__isnull=True) \
        .values_list("assigned_to_group__name", flat=True)
    keywords = forms.filter(keywords__isnull=False) \
        .values_list("keywords", flat=True).order_by()
    safetycube = []
    try:
        if forms.first().options.is_safetycube_enabled() and \
                forms.filter(safetycube__reference__isnull=False).exists():
            safetycube = [{'label': "Oui", 'value': 'true'},
                          {'label': "Non", "value": "false"}]
    except:
        pass
    return {
        "count": forms.count(),
        "zones": sorted(zones.order_by().distinct()),
        "statuses": sorted(statuses.order_by().distinct()),
        "assigned_to": sorted(groups.order_by().distinct()),
        "safetycube": safetycube,
        "keywords": sorted(set(
            [tag for k in keywords for tag in k.split(" ") if tag]))
    }
