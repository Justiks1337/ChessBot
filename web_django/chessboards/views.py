from django.http import HttpRequest

from asyncio import sleep
from django.http import HttpResponse


async def index(request: HttpRequest):
	await sleep(10)
	return HttpResponse('test')


def player_mode(request: HttpRequest):
	pass


def spectator_mode(request: HttpRequest):
	pass



