# XV6n 服务器后端


## 运行

```bash
> pacman -S postgresql-libs  # On arch
> # or
> apt install libpq5  # On ubuntu/debian

> pip install -r requirements.txt
> python -m uvicorn main:app --reload
```