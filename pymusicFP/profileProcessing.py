def displace_profiles_by_key(offset: int, profiles_dict: dict) -> dict:
    profiles = {}
    if offset == 0:
        return profiles_dict
    for profile in profiles_dict:
        profiles[profile] = []
        [profiles[profile].append(prefix) for prefix in profiles_dict[profile][-offset:]]
        [profiles[profile].append(suffix) for suffix in profiles_dict[profile][0:-offset]]
    return profiles


def profiles_distance(main_profile: list[float], profiles_dict: dict) -> dict:
    distances = {}
    for profile in profiles_dict:
        squared_dist = 0
        for index in range(len(profiles_dict[profile])):
            squared_dist += (main_profile[index] - profiles_dict[profile][index]) ** 2
        distances[profile] = squared_dist ** (1 / 2)
    return distances
