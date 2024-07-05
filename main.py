from fastapi import FastAPI
import todos, auth, users, profile, note, post, e_commerce

app = FastAPI()

routers = [
    todos.router,
    auth.router,
    users.router,
    profile.router,
    note.router,
    post.router,
    e_commerce.router,
]

for router in routers:
    app.include_router(router)
