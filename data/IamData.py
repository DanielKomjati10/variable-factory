import boto3


session = boto3.session.Session(profile_name='wheel')
iam = session.client('iam')


class IamData:


    def __init__(self):
        self.users = self.__get_user_data()
        self.groups = self.__get_group_data()
        self.policies = self.__get_policy_data()


###############################################################################################################
# Private:
###############################################################################################################


    def __get_policy_data(self):
        policies_per_group = []
        for group in self.groups:
            current_group = {}
            current_group["GroupName"] = group["GroupName"]
            current_group["Policies"] = []
            for policy in iam.list_attached_group_policies(GroupName=group["GroupName"])['AttachedPolicies']:
                current_policy = {}
                for key in ["PolicyName", "PolicyArn"]:
                    current_policy[key] = policy[key]
                current_group["Policies"].append(current_policy)
            policies_per_group.append(current_group)
        return policies_per_group


    def __get_group_data(self):
        existing_groups = []
        for group in iam.list_groups()["Groups"]:
            current_group = {}
            for attribute in ["GroupName", "GroupId", "Arn"]:
                current_group[attribute] = group[attribute]
            existing_groups.append(current_group)
        return existing_groups


    def __get_user_data(self):
        all_users = []
        for user in iam.list_users()['Users']:
            current_user = {}
            for attribute in ["UserName", "Arn"]:
                current_user[attribute] = user[attribute]
            current_user["Groups"] = []
            for group_name in iam.list_groups_for_user(UserName=user['UserName'])['Groups']:
                current_user["Groups"].append(group_name['GroupName'])
            all_users.append(current_user)
        return all_users


###############################################################################################################
# Public:
###############################################################################################################


    def get_users(self):
        return self.users
    

    def get_groups(self):
        return self.groups


    def get_policies(self):
        return self.policies


#    def set_users(self):
#        self.users = self.__get_user_data()


#    def set_groups(self):
#        self.groups = self.__get_group_data()


#    def set_policies(self):
#        self.policies = self.__get_policy_data()


    def display_data(self, iam_entities, entity_type):
        print(f"-----------\n\n# {entity_type}:\n")
        for entity in iam_entities:
            print(str(entity))
        print(f"\nNumber of {entity_type.lower()} is: {len(iam_entities)}")
