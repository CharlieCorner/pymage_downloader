IMGUR_PARAMS_CLIENT_ID = "client_id"
IMGUR_PARAMS_API_CALLS_LIMITS = "api_calls_limits"
IMGUR_PARAMS_API_CALLS_LIMITS_USER_LIMIT = "user_limit"
IMGUR_PARAMS_API_CALLS_LIMITS_USER_REMAINING = "user_remaining"
IMGUR_PARAMS_API_CALLS_LIMITS_USER_RESET_TIMESTAMP = "user_reset_timestamp"
IMGUR_PARAMS_API_CALLS_LIMITS_CLIENT_LIMIT = "client_limit"
IMGUR_PARAMS_API_CALLS_LIMITS_CLIENT_REMAINING = "client_remaining"

IMGUR_PARAMS = {
    IMGUR_PARAMS_CLIENT_ID: "",
    IMGUR_PARAMS_API_CALLS_LIMITS: {
        IMGUR_PARAMS_API_CALLS_LIMITS_USER_LIMIT: 1000000,
        IMGUR_PARAMS_API_CALLS_LIMITS_USER_REMAINING: 1000000,
        IMGUR_PARAMS_API_CALLS_LIMITS_USER_RESET_TIMESTAMP: -1,
        IMGUR_PARAMS_API_CALLS_LIMITS_CLIENT_LIMIT: 1000000,
        IMGUR_PARAMS_API_CALLS_LIMITS_CLIENT_REMAINING: 1000000
    }
}

IMGUR_LIMIT_WARNING_THRESHOLD = 15

IMGUR_GALLERY = "gallery"
IMGUR_ALBUM = "album"
IMGUR_SIMPLE = "simple"
IMGUR_ID = "{{imgur_id}}"

IMGUR_ENDPOINTS = {
    IMGUR_GALLERY: "",
    IMGUR_ALBUM: "",
    IMGUR_SIMPLE: "https://api.imgur.com/3/image/{{imgur_id}}"
}

IMGUR_API_RESPONSE_HEADER_USER_LIMIT = "X-RateLimit-UserLimit"
IMGUR_API_RESPONSE_HEADER_USER_REMAINING = "X-RateLimit-UserRemaining"
IMGUR_API_RESPONSE_HEADER_USER_RESET = "X-RateLimit-UserReset"

HTTP_HEADER_AUTHORIZATION = "Authorization"
