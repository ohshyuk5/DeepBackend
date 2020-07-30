# DeepBackend
## API List
---
1. user

    POST    /user/              -> 유저 정보 저장
    GET     /user/{user_id}     -> 유저 정보 요청: 개발용 api
    DELETE  /user/{user_id}     -> 유저 정보 삭제

2. media

    POST    /media/             -> 합성 요청 (유저 id, 사진, 영상)
    GET     /media/{user_id}    -> 결과 영상 요청
    DELETE  /media/{user_id}    -> 정보 삭제

## Flow
---
1. 서버에 유저 등록
2. 앱은 서버에서 uid 받음
3. 서버는 DB에 유저 정보 등록
4. 앱은 서버에 합성 요청
5. 서버는 앱에 rid 발급
6. 앱은 스토리지에 User/uid/Request/rid/ 에 video, photo 저장
7. 서버는 storage에서 video와 photo 불러옴
8. 서버는 합성 후 결과물을 스토리지에 저장
9. 스토리지는 저장이 되면 앱에 알림
10. 앱은 스토리지에 결과물 요청
11. 스토리지는 앱에 결과물 전송

