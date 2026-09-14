import re


check_password = input("Enter a password to check(You should enter at least 8 characters): ")
'''
def check_len(pss):
    if len(pss) < 8:
        return "Password is too short"
    if len(pss) > 50:
        return "Password is too long"
    return "Your Password is pass"
'''
def check_len_valid(pss):
    if len(pss) < 8:
        return False
    if len(pss) > 50:
        return False
    return True

def check_upper(pss):
    return bool(re.search(r'[A-Z]', pss))

def check_lower(pss):
    return bool(re.search(r'[a-z]', pss))

def check_digit(pss):
    return bool(re.search(r'[0-9]', pss))

def check_special(pss):
    return bool(re.search(r'[^0-9A-Za-z]', pss))

def check_repeat(pss):
    if len(pss) == 0:
        return 0
    unique_chars = len(set(pss))
    return unique_chars / len(pss)

def calculate_score(pss):
    if not check_len_valid(pss):
        return 0
    score = 0
    if len(pss) >= 8:
        score += 1
    if len(pss) >= 12:
        score += 1

    if len(pss) >= 16:
        score += 1

    if check_upper(pss):
        score += 1

    if check_lower(pss):
        score += 1  

    if check_digit(pss):
        score += 1  

    if check_special(pss):
        score += 1

    repeat_ratio = check_repeat(pss)
    
    if repeat_ratio < 0.3:
        score -= 2  
    elif repeat_ratio < 0.5:
        score -= 1  
    else:
        score = 1
    return max(score, 0)

def check_password_strength(pss):
    score = calculate_score(pss)
    if score >= 5:
        return "Very strong password"
    elif score >= 4:
        return "Strong password"
    elif score >= 3:
        return "Moderate password"
    elif score >= 2:
        return "Weak password"
    else:
        return "Very weak password"



def estimate_crack_time(pss):
    if not pss:
        return "No password provided"

    pool_size = 0
    if check_upper(pss):
        pool_size += 26

    if check_lower(pss):
        pool_size += 26

    if check_digit(pss):
        pool_size += 10 

    if check_special(pss):
        pool_size += 32

    repeated = 0
    for i in range(1, len(pss)):
        if pss[i] == pss[i-1]:
            repeated += 1
    repeat_ratio = repeated / len(pss)

    effective_length = len(pss) * (1 - repeat_ratio)
    effective_length = max(effective_length, 1)

    total_combinations = pool_size ** effective_length
    seconds = total_combinations / 10000000000
    





    if seconds < 60:
        return f"{int(seconds)} seconds"    

    elif seconds < 3600:
        return f"{int(seconds / 60)} minutes"

    elif seconds < 86400:
        return f"{int(seconds / 3600)} hours"

    elif seconds < 31536000:
        return f"{int(seconds / 86400)} days"

    elif seconds < 3153600000:
        return f"{int(seconds / 31536000)} years"

    else:
        return f"{int(seconds / 3153600000)} centuries"







q = check_password_strength(check_password)
w = estimate_crack_time(check_password)
print(q)
print(w)
