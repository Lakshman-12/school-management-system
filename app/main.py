from contextlib import asynccontextmanager
from fastapi import FastAPI
import logging


from app.modules.auth.router import router as auth_router
from app.modules.teachers.router import router as teachers_router
from app.modules.classes.router import router as classes_router
from app.modules.subjects.router import router as subjects_router
from app.modules.teacher_assignments.router import router as teacher_assignment_router
from app.middleware.timing import add_process_time_header
from app.middleware.logging import log_requests




@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: runs before the app accepts requests
    print("School Management System is starting...")

    yield

    # Shutdown: runs when the app shuts down
    print("School Management System is shutting down...")
    
    
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s",
)


app = FastAPI(
    title="School Management System",
    description="End-to-end School Management API",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(auth_router)
app.include_router(teachers_router)
app.include_router(classes_router)
app.include_router(subjects_router)
app.include_router(teacher_assignment_router)
app.middleware("http")(add_process_time_header)
app.middleware("http")(log_requests)