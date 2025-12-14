import uvicorn

print("=" * 60)
print("Starting Medical Report Generator...")
print("=" * 60)
print("\nServer will be available at:")
print("- http://localhost:8000")
print("- http://localhost:8000/docs (API documentation)")
print("\nPress CTRL+C to stop the server\n")
print("=" * 60)

# Run the FastAPI app
if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=False)
