def initial_session(request, user):
    permissions = user.roles.all().values("permissions__url", "permissions__group_id", "permissions__action").distinct()
    print(permissions)
    permission_dict = {}
    for item in permissions:
        gid = item.get('permissions__group_id')
        if not gid in permission_dict:
            permission_dict[gid] = {
                "urls": [item["permissions__url"], ],
                "actions": [item["permissions__action"], ]
            }
        else:
            permission_dict[gid]['urls'].append((item["permissions__url"]))
            permission_dict[gid]['actions'].append(item["permissions__action"])
    print(permission_dict)
    request.session["permission_dict"] = permission_dict
