def build_response(status: str, data: dict | list ) -> dict:
    return {"status" :status, "data" : data}