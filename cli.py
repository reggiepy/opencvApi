# *_*coding:utf-8 *_*
# @Author : Reggie
# @Time : 2023/7/2 16:32
import argparse
import datetime
import json
import shutil
import shelve
from pathlib import Path

from common_api.user import UserApi
from models.user import UserUpdate

VERSION = "v1.0.0"

BASE_PATH = Path(__file__).parent


class Cli:

    @classmethod
    def updateUserLoginData(cls, parse_args):
        user_name = parse_args.user_name
        user_id = parse_args.user_id
        if not any([user_name, user_id]):
            raise ValueError("required user name or user id")
        if user_name:
            user_obj, msg, rc = UserApi.get_user_by_name(user_name)
            if rc:
                raise ValueError(f"get user by name failed: {msg}")
            user_id = user_id.id
        else:
            user_obj, msg, rc = UserApi.get_user(user_id)
            if rc:
                raise ValueError(f"get user by name failed: {msg}")
        with open(f"loginUser_{user_obj.name}.json", "r", encoding="utf-8") as f:
            format_json = json.dumps(json.load(f))
            update_info = UserUpdate(login_data=format_json)
            _, msg, rc = UserApi.update_user(user_id, update_info)
            if rc:
                print("update user failed: {msg}")

    @classmethod
    def updateUserLoginDataToken(cls, parse_args):
        user_name = parse_args.user_name
        user_id = parse_args.user_id
        token = parse_args.token
        if not any([user_name, user_id]):
            raise ValueError("required user name or user id")
        if user_name:
            user_obj, msg, rc = UserApi.get_user_by_name(user_name)
            if rc:
                raise ValueError(f"get user by name failed: {msg}")
            user_id = user_id.id
        else:
            user_obj, msg, rc = UserApi.get_user(user_id)
            if rc:
                raise ValueError(f"get user by name failed: {msg}")
        update_info = UserUpdate(token=token)
        _, msg, rc = UserApi.update_user(user_id, update_info)
        if rc:
            print("update user failed: {msg}")
            return

        with open(f"loginUser_{user_obj.name}.json", "r", encoding="utf-8") as f:
            login_data = json.load(f)
            login_data["data"]["token"] = token

        with open(f"loginUser_{user_obj.name}.json", "w", encoding="utf-8") as f:
            f.write(json.dumps(login_data, ensure_ascii=False, indent=4))

    @classmethod
    def archived_logs(cls, parse_args):
        """
        归档
        :return:
        """
        ignore_files = [
            "db.log",
            "fastapi_access.log",
            "fastapi_error.log",
            "root.log",
            "yongfeng.log",
            ".gitkeep",
        ]

        def is_ignore(filename):
            for igf in ignore_files:
                if item.name.startswith(igf):
                    print(f"ignore {item}")
                    return True
            return False

        now = datetime.datetime.now()
        now_date = now.strftime("%Y-%m-%d")
        archived_path = Path("归档").joinpath(f"logs {now_date}")
        archived_path.mkdir(parents=True, exist_ok=True)
        for item in Path(BASE_PATH).joinpath("logs").iterdir():
            if is_ignore(item):
                continue
            if item.is_file():
                print(f"{item.absolute()}---->{archived_path.absolute()}")
                shutil.move(item.absolute().as_posix(), archived_path.absolute().as_posix())


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--version", action="version", version=VERSION, help="show version")
    parser.set_defaults(func=lambda _: parser.print_help())

    subparsers = parser.add_subparsers(title="subparsers")

    # ############################### User ####################################
    user_parser = subparsers.add_parser("user", help="user cmd")
    user_parser.set_defaults(func=lambda _: user_parser.print_help())

    user_subparsers = user_parser.add_subparsers(title="user sub commands")
    update_user_info_parser = user_subparsers.add_parser("update_login_info", help="update user login info")
    update_user_info_parser.add_argument("-un", "--user_name", required=False, type=str, help="user name")
    update_user_info_parser.add_argument("-ui", "--user_id", required=False, type=int, help="user id")
    update_user_info_parser.set_defaults(func=Cli.updateUserLoginData, parser=user_parser)

    update_user_info_parser = user_subparsers.add_parser("update_token", help="update user login info")
    update_user_info_parser.add_argument("-un", "--user_name", required=False, type=str, help="user name")
    update_user_info_parser.add_argument("-ui", "--user_id", required=False, type=int, help="user id")
    update_user_info_parser.add_argument("-tk", "--token", required=True, type=str, help="token")
    update_user_info_parser.set_defaults(func=Cli.updateUserLoginDataToken, parser=user_parser)

    # ############################### User ####################################
    archived_parser = subparsers.add_parser("archived", help="archived cmd")
    archived_parser.set_defaults(func=lambda _: archived_parser.print_help())

    archived_logs_subparsers = archived_parser.add_subparsers(title="archived logs commands")
    archived_logs_parser = archived_logs_subparsers.add_parser("logs", help="archived logs")
    archived_logs_parser.set_defaults(func=Cli.archived_logs, parser=archived_logs_parser)

    parse_args = parser.parse_args()
    parse_args.func(parse_args)