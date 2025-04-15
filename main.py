from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Import routers
from routes.RoleRoutes import router as role_router
from routes.UserRoutes import router as user_router
from routes.StateRoutes import router as state_router
from routes.CityRoutes import router as city_router
from routes.AreaRoutes import router as area_router
from routes.CategoryRoutes import router as category_router
from routes.SubCategoryRoutes import router as sub_category_router
from routes.ProductRoutes import router as product_router
from routes.CarRoutes import router as car_router
from routes.CarDetailsRoutes import router as car_details_router
from routes.auth_routes import router as auth_router
from routes.profile_routes import router as profile_router
from routes.AgentRoutes import router as agent_router

from config.database import user_collection, role_collection
from bson import ObjectId

app = FastAPI()

# Middleware to handle exceptions globally
@app.middleware("http")
async def debug_request_middleware(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except Exception as e:
        logger.error(f"Request failed: {str(e)}")
        return Response(
            content=f"Internal server error: {str(e)}",
            status_code=500,
        )

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
app.include_router(category_router, prefix="/api/categories", tags=["Categories"])
app.include_router(sub_category_router, prefix="/api/subcategories", tags=["Subcategories"])
app.include_router(product_router, prefix="/api/products", tags=["Products"])
app.include_router(car_router, prefix="/api/cars", tags=["Cars"])
app.include_router(car_details_router, prefix="/api/car-details", tags=["Car Details"])
app.include_router(auth_router)  # ✅ Authentication Routes
app.include_router(profile_router, prefix="/api", tags=["Profile"])  # ✅ Profile Routes
app.include_router(agent_router, prefix="/api/agents", tags=["Agents"])  # Agent Routes

# ✅ Get all users (test/debug endpoint)
@app.get("/users")
async def get_users():
    users = await user_collection.find().to_list(length=100)
    return [{"id": str(user["_id"]), "name": user["name"], "email": user["email"]} for user in users]

# ✅ Role Management Routes for quick fixes
@app.post("/api/fix-roles")
async def fix_missing_roles():
    """Emergency endpoint to create missing roles and fix users without roles"""
    # Create roles if they don't exist
    role_names = ["Admin", "User", "Agent"]
    role_ids = {}
    
    for role_name in role_names:
        existing_role = await role_collection.find_one({"name": role_name})
        if existing_role:
            role_ids[role_name] = existing_role["_id"]
        else:
            result = await role_collection.insert_one({"name": role_name})
            role_ids[role_name] = result.inserted_id
    
    # Find users without roles and assign them the "User" role
    users_without_role = await user_collection.find({"role_id": {"$exists": False}}).to_list(length=None)
    updated_count = 0
    
    for user in users_without_role:
        await user_collection.update_one(
            {"_id": user["_id"]},
            {"$set": {"role_id": role_ids["User"]}}
        )
        updated_count += 1
    
    return {"message": f"Roles created: {list(role_ids.keys())}, Users updated: {updated_count}"}

@app.post("/api/assign-role/{user_id}/{role_name}")
async def assign_role_to_user(user_id: str, role_name: str):
    """Assign a role to a specific user"""
    try:
        # Check if user exists
        user = await user_collection.find_one({"_id": ObjectId(user_id)})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Check if role exists
        role = await role_collection.find_one({"name": role_name})
        if not role:
            # Create the role if it doesn't exist
            result = await role_collection.insert_one({"name": role_name})
            role_id = result.inserted_id
        else:
            role_id = role["_id"]
        
        # Assign role to user
        await user_collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"role_id": role_id}}
        )
        
        return {"message": f"Role '{role_name}' assigned to user successfully"}
    except Exception as e:
        logger.error(f"Error assigning role: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to assign role: {str(e)}")

# ✅ Run the server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)