import json
import os
import re
from enum import Enum


class PROFILE_RET(Enum):
    OK = 0,
    DUPLICATE = 1,
    FAILURE = 2

# class Profile:
#     def __init__(self, name):
#         self.name = name
#         self.label = 0

#     def json(self):
#         return dict({"name": self.name})

#     def __eq__(self, __o: object) -> bool:
#         if isinstance(__o, Profile):
#             return self.name == __o.name
#         if isinstance(__o, str):
#             return self.name == __o
#         raise RuntimeError("Can't compare object of type 'Profile' to object og type '", type(__o), "'")


class Profiles:
    def __init__(self):
        self.profiles = None
        self.read_profiles()

    def json(self):
        if self.profiles is None:
            return ""
        r = []
        [r.append({"name": k, "label": v}) for k, v in self.profiles.items()]
        return {"profiles": r}

    def add_profile(self, name: str):
        name = name
        if self.profiles is not None:
            if name not in self.profiles:
                self.profiles[name] = 0
                self.flush()
                return (PROFILE_RET.OK, "Added profile '" + name + "'")
            else:
                return (PROFILE_RET.DUPLICATE, "Profile '" + name + "' already exists")
        else:
            return (PROFILE_RET.FAILURE, "Read in the profiles before accessing them")

    def remove_profile(self, id: str):
        if self.profiles is not None:
            deleted_key = self.profiles.pop(id, None)
            if deleted_key is not None:
                [
                    os.remove('dataset/' + file)
                    for file in os.listdir('dataset/')
                    if re.search("User." + id + ".[0-9]+.jpg", file)
                ]

                self.flush()
                return (True, "Removed profile '" + id + "'")
            else:
                return (True, "Profile '" + id + "' not found")
        else:
            return (False, "Read in the profiles before accessing them")

    def read_profiles(self, overwrite=False):
        if self.profiles is not None and overwrite is False:
            print("Profiles have already been readed, use override flag")
            return
        self.profiles = {}
        json_profiles = self.generator_profiles()
        for profile in json_profiles:
            self.profiles[profile["name"]] = profile["label"]

    def flush(self):
        with open("profiles.json", mode="w") as f:
            json.dump(self.json(), f, indent=4)
        self.changed = False

    def generator_profiles(self):
        with open("src/real_time_face_detection/ressources/profiles.json", "r") as f:
            profiles = json.load(f)
        for profile in profiles["profiles"]:
            yield profile


# Simple test routine
def test():
    import os

    init_size = os.path.getsize('profiles.json')

    profiles = Profiles()
    r = profiles.add_profile("case")
    print(r[1])
    r = profiles.add_profile("case")
    print(r[1])
    r = profiles.remove_profile("case")
    print(r[1])
    r = profiles.remove_profile("case")
    print(r[1])

    assert init_size == os.path.getsize('profiles.json')
