from zxcvbn import zxcvbn

def check_password_strength(pas):
    
    if len(pas) < 8:
        return "Password is too short"
    if len(pas) > 50:
        return "Password is too long"

    result = zxcvbn(pas)
    score = result['score'] #

    ratings = {
        0: "Very weak password",
        1: "Weak password",
        2: "Moderate password",
        3: "Strong password",
        4: "Very strong password"
    }

    return ratings[score]


def estimate_crack_time(pas):
    result = zxcvbn(pas)
    seconds = result['crack_times_seconds']['offline_slow_hashing_1e4_per_second']

    if seconds < 60:
        return f"{int(seconds)} seconds"
    elif seconds < 3600:
        return f"{int(seconds / 60)} minutes"
    elif seconds < 86400:
        return f"{int(seconds / 3600)} hours"
    elif seconds < 31536000:
        return f"{int(seconds / 86400)} days"
    else:
        return f"{int(seconds / 31536000)} years"











