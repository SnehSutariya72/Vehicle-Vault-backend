from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

# Import routers
from routes.RoleRoutes import router as role_router
from routes.UserRoutes import router as user_router
from routes.StateRoutes import router as state_router
from routes.CityRoutes import router as city_router
from routes.AreaRoutes import router as area_router
# from routes.AgentRoutes import router as agent_router  # 🛠 Optional: Uncomment if needed
from routes.CategoryRoutes import router as category_router
from routes.SubCategoryRoutes import router as sub_category_router
from routes.ProductRoutes import router as product_router
from routes.CarRoutes import router as car_router
from routes.CarDetailsRoutes import router as car_details_router
from routes.auth_routes import router as auth_router
from routes.profile_routes import router as profile_router  # ✅ Import profile routes

from config.database import user_collection

app = FastAPI()

# ✅ Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Serve static files (e.g., car/property images)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# ✅ Include API routes
app.include_router(role_router, prefix="/api/roles", tags=["Roles"])
app.include_router(user_router, prefix="/api/users", tags=["Users"])
app.include_router(state_router, prefix="/api/states", tags=["States"])
app.include_router(city_router, prefix="/api/cities", tags=["Cities"])
app.include_router(area_router, prefix="/api/areas", tags=["Areas"])
# app.include_router(agent_router, prefix="/api/agents", tags=["Agents"])  # 🛠 Optional
app.include_router(category_router, prefix="/api/categories", tags=["Categories"])
app.include_router(sub_category_router, prefix="/api/subcategories", tags=["Subcategories"])
app.include_router(product_router, prefix="/api/products", tags=["Products"])
app.include_router(car_router, prefix="/api/cars", tags=["Cars"])
app.include_router(car_details_router, prefix="/api/car-details", tags=["Car Details"])
app.include_router(auth_router)  # ✅ Authentication Routes
app.include_router(profile_router, prefix="/api", tags=["Profile"])  # ✅ Profile Routes

# ✅ Get all users (test/debug endpoint)
@app.get("/users")
async def get_users():
    users = await user_collection.find().to_list(length=100)
    return [{"id": str(user["_id"]), "name": user["name"], "email": user["email"]} for user in users]

# ✅ Run the server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
