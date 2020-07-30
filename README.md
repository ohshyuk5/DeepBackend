# DeepBackend
## API List
---
1. user

    POST    /user/              -> 유저 정보 저장(user_name, password, ...)
    GET     /user/{user_id}     -> 유저 정보 요청(아마 삭제 예정)
    PUT     /user/{user_id}     -> 저장된 유저 정보 변경
    DELETE  /user/{user_id}     -> 유저 정보 삭제

2. media

    POST    /media/             -> 합성 요청 (유저 id, 사진, 영상)
    GET     /user
    DELETE
