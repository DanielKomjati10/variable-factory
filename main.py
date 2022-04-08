import os
from data import IamData
from jinja2 import Environment, FileSystemLoader


def create_aws_group_tfvars(policies):
    env = Environment(
        loader=FileSystemLoader("templates/"),
        autoescape=True
    )
    template = env.get_template("terraform.tfvars.j2")
    parsed_template = template.render(policies=policies)

    with open("terraform.tfvars", "w") as tfvars:
        tfvars.write(parsed_template)


def main():
    print("## AWS CLI authentication...\n")
    os.system("aws-mfa")
    print("\n## AWS IAM Data:")

    iam = IamData.IamData()
    # Get users:
    users = iam.get_users()
    iam.display_data(users, "Users")

    # Get groups:
    groups = iam.get_groups()
    iam.display_data(groups, "Groups")

    # Get policies per group:
    policies = iam.get_policies()
    iam.display_data(policies, "Groups and policies")

    # Render tfvars from template:
    create_aws_group_tfvars(policies=policies)


if __name__ == "__main__":
    main()
