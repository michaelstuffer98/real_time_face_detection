import json

from numpy import isin

class Profile:
    def __init__(self, name, id):
        self.name = name
        self.id = id
    
    def json(self):
        return dict({"name": self.name, "id": self.id })

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Profile):
            return self.id == __o.id
        if isinstance(__o, int):
            return self.id == __o
        raise RuntimeError("Can't compare object of type 'Profile' to object og type '", type(__o), "'")

class Profiles:
    def __init__(self):
        self.profiles = None
        pass

    def json(self):
        return dict({"profiles": [ p.json() for p in self.profiles ]})

    def add_profile(self, profile: Profile):
        if not self.profiles is None:
            if profile in self.profiles:
                return (False, "Duplicate Profile id")
            self.profiles.append(profile)
            self.flush()
            return (True, "Added profile")
        else:
            return (False, "Read in the profiles before accessing them")

    def remove_profile(self, id):
        if not self.profiles is None:
                [ os.remove('dataset/' + file) for file in os.listdir('dataset/') if re.search("User." + id + ".[0-9]+.jpg", file) ]
                self.flush()
                return (True, "Removed profile")
            else:
                return (True, "Profile id not found")
        else:
            return (False, "Read in the profiles before accessing them")

    def read_profiles(self):
        self.profiles = []
        json_profiles = self.generator_profiles()
        for profile in json_profiles:
            self.profiles.append(Profile(profile["name"], profile["id"]))

    def flush(self):
        with open("profiles.json", mode="w") as f:
            json.dump(self.json(), f, indent = 4)
        self.changed = False

    def generator_profiles(self):
        with open("profiles.json", "r") as f:
            profiles = json.load(f)
        for profile in profiles["profiles"]:
            yield profile

profiles = Profiles()
profiles.read_profiles()
profiles.remove_profile(7)