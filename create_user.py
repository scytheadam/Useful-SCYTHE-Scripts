import scythe_helpers.auth as helpers


if __name__ == '__main__':
    print("Running...\n")
    # Optional/helper way to get SCYTHE Credentials via argparse ...
    parser = helpers.setup_cred_args()
    args = parser.parse_args()

    # Use the optional helper for arguments ...
    SCYTHE_API = helpers.login(
        args.scythe_dest,
        args.scythe_user,
        args.scythe_pass,
    )

    # Get all users (via /RPC1)
    result = SCYTHE_API["rpc1"].get_users()
    print("Current amount of users: %s" % len(result))

    # Example User Object, with non-admin roles
    example_user = {
        'username': "jdoe",
        'firstname': "Jesse",
        'lastname': "Doe",
        'email': "jdoe@fakecorp.com",
        'password': "temporarypassword",
        'roles': [
            'LOCALIZED_ROLE_ITEM_CAMPAIGNS_DELETE',
            'LOCALIZED_ROLE_ITEM_REPORTS_VIEW',
            'LOCALIZED_ROLE_ITEM_THREATS_VIEW',
            'LOCALIZED_ROLE_ITEM_THREATS_CREATE',
            'LOCALIZED_ROLE_ITEM_THREATS_UPDATE',
            'LOCALIZED_ROLE_ITEM_CAMPAIGNS_CREATE',
            'LOCALIZED_ROLE_ITEM_VFS_VIEW',
            'LOCALIZED_ROLE_ITEM_VFS_WRITE',
            'LOCALIZED_ROLE_ITEM_VFS_MODIFY',
            'LOCALIZED_ROLE_ITEM_VFS_DELETE',
            'LOCALIZED_ROLE_ITEM_THREATS_DELETE'
        ]
    }
    print("\nAttempting creation of user '%s' ..." % example_user['username'])

    # Create user ...
    result = SCYTHE_API["rpc1"].add_user(
        example_user['username'],
        example_user['firstname'],
        example_user['lastname'],
        example_user['email'],
        example_user['password'],
        example_user['roles']
    )
    if result == "LOCALIZED_INFO_USER_CREATED":
        print("Success!")
    else:
        print("Failed. Error: %s" % result)

    # Get all users (via /RPC1) ... again
    result = SCYTHE_API["rpc1"].get_users()
    print("\nNew amount of users: %s" % len(result))

    print("\n ...Exiting.\n")
    exit()
