from src.api.guest import controller as guest_controller
from src.api.user import controller as user_controller
from src.api.news import controller as news_controller


def cors_setting(app, CORSMiddleware):
    origins = [
        "*"
    ]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def url_routing_check(request):
    request_url = str(request.url)
    print("############# request_url : ", request_url)


def router_setting(app, master_router, guest_router, user_router, news_router):
    guest_router.include_router(guest_controller.router)
    user_router.include_router(user_controller.router)
    news_router.include_router(news_controller.router)

    master_router.include_router(guest_router)
    master_router.include_router(user_router)
    master_router.include_router(news_router)
    app.include_router(master_router)
