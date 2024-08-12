# Actions
def make_verified(modeladmin, request, queryset):
    queryset.update(is_verified=True)
make_verified.short_description = 'Mark selected users as verified'

def make_unverified(modeladmin, request, queryset):
    queryset.update(is_verified=False)
make_unverified.short_description = 'Mark selected users as unverified'

def make_public_account(modeladmin, request, queryset):
    queryset.update(is_public_account=True)
make_public_account.short_description = 'Mark selected users as public accounts'

def make_private_account(modeladmin, request, queryset):
    queryset.update(is_public_account=False)
make_private_account.short_description = 'Mark selected users as private accounts'


def delete_location_info(modeladmin, request, queryset):
    queryset.update(location_url=None)
    queryset.update(location=None)
delete_location_info.short_description = 'Delete location information from selected posts'