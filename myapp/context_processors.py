def streak_context(request):
    if request.user.is_authenticated:
        profile = request.user.profile
        return {"daily_streak": profile.daily_streak}
    return {}
