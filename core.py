from exceptions.OnEndTimeError import OnEndTimeError


def on_end_time_error(*args, **kwargs):
	print(args)
	print(kwargs)
	raise OnEndTimeError(kwargs["color"])
