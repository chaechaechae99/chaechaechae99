# 프로필 움짤 만드는 코드

프로필 README에 들어가는 도트 애니메이션(SVG)을 코드로 찍어서 만든다.

| 파일 | 만드는 것 |
|---|---|
| `gen.py` | 오락실(`b-arcade.svg`), 상태창(`player.svg`), 그리고 안 쓰는 시안 2개 |
| `strips.py` | STAGE마다 들어가는 한 줄 움짤 (`stage1-airport.svg` ...) |

## 실행

```
pip install fonttools brotli pillow
python tools/gen.py out
python tools/strips.py "<airport-rookie 폴더 경로>" out
```

`out` 폴더에 SVG가 생긴다. 고친 그림은 `assets/`에 **새 이름(-v2, -v3...)**으로 넣고 README 경로도 바꿔야 브라우저 캐시 때문에 옛 그림이 안 보인다.

`strips.py`의 공항 움짤은 airport-rookie 저장소의 `sprites.py`(실제 게임 그림)를 불러다 쓴다.

## 폰트

- [Galmuri](https://github.com/quiple/galmuri) — SIL Open Font License 1.1
- [Press Start 2P](https://fonts.google.com/specimen/Press+Start+2P) — SIL Open Font License 1.1

SVG 안에는 실제로 쓴 글자만 잘라서 넣는다.
