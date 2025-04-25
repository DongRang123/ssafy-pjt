# Info

### 기본 정보

- Front Framework : (추후 Vue 예정)
- Back Framework : Django
- 제공 데이터 양식 : JSON

### Models

- <b>accounts</b> : Custom accounts 사용
- <b>book</b> : 제목, 카테고리, ISBN, 설명, cover image, 출판사, 출판일자, 저자 등
- <b>threads</b> : 도서(FK), 글 제목, 내용, 독서일자
- <b>comments</b> : 스레드(FK), 댓글 제목, 내용

### URLS

현재 URL은 REST하지 않습니다. (추후 수정 예정)
| URL | 대상 | HTTP methods |
| ----- | ------ | ------------- |
|`books/`| 전체 도서 조회 / 도서 생성 | `GET, POST` |
|`books/<int:book_pk>`| 도서 상세 조회 / 수정 / 삭제 | `GET, PUT, DELETE` |
|`threads/`| 전체 쓰레드 조회 | `GET` |
|`<int:book_pk>/threads/`| 쓰레드 생성 | `POST` |
|`threads/<int:thread_pk>/`| 쓰레드 상세 조회 / 수정 / 삭제 | `GET, PUT, DELETE` |
|`threads/<int:thread_pk>/comments/`| 코멘트 생성 | `POST` |
|`comments/<int:comment_pk>/`| 코멘트 조회 / 수정 / 삭제 | `GET, PUT, DELETE` |
<br><br>
