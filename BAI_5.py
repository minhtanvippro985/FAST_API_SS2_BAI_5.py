


from fastapi import FastAPI , HTTPException,status
from pydantic import BaseModel

app = FastAPI()

class Books(BaseModel):
    id : int
    name: str
    price : float
    sold : int


book_list = [
    {
     "id" : 1 ,
     "name" : "Lmao",
     "price" : 12123123.2,
     "sold" : 4
     },
    {
     "id" : 2 ,
     "name" : "hádasdadsads",
     "price" : 523.2,
     "sold" : 2
     },
]

@app.get("/books")
def get_all_books():
    if len(book_list) == 0:
        return {
            "message" : "Hiện chưa có sách nào",
            "data" : []
        }
    else:
        return  {
            "message" : "Danh sách sách có trong hệ thống",
            "data" : book_list
        }

@app.get("/book/details/{id}")
def get_book_detail(id :int):
    for book_s in book_list:
        if book_s['id'] == id:
            return{
                "message" : f"Chi tiết cuốn sách {id}",
                "data" : book_s
            }
    
    return {
        "message" : f"Không tìm thấy sách nào có id {id}",
        "data" : []
    }



@app.post("/add_book/", status_code=status.HTTP_201_CREATED)
def create_item(item: Books):
    # chuyển dữ liệu mới nhận được thành một dict
    new_book = item.model_dump()
    
    for book in book_list:
        if book["id"] == new_book["id"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail=f"{new_book['id']} đã tồn tại trong hệ thống!"
            )
        
            
    #  tiến hành thêm vào kho
    book_list.append(new_book)
    
    return {
        "message": "Thêm sản phẩm thành công!",
        "data": new_book,
        "kho_hien_tai": book_list
    }


@app.put("/edit_book/{book_id}")
def update_item(book_id: int, item_update: Books):
    target_index = None
    
    for index, item in enumerate(book_data):
        if item["id"] == book_id:
            target_index = index
            break
            
    if target_index is None:
        raise HTTPException(status_code=404, detail="Không tìm thấy sản phẩm cần sửa")

    book_data = item_update.model_dump()
    
    for index, item in enumerate(book_list):
        if index == target_index:
            continue
            
        if item["id"] == book_data["id"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Không thể cập nhật vì ID {book_data['id']} đã được dùng "
            )
            
     

    book_list[target_index] = book_data
    
    return {
        "message": "Cập nhật thông tin thành công!",
        "data_updated": book_data,
        "kho_hien_tai": book_list
    }

@app.delete("/books/delete{id}")
def delete_books(id :int):
    for book in book_list:
        if book['id'] == id:
            book_list.remove(book)
            return{
                "message" : f"Đã xóa thành công sách có {id} ,danh sách hiện tại" ,
                "data" : book_list
            }
    
    return{
        "message" :f"Không tìm thấy sách có {id}",
        "data" : book_list
    }

@app.get("/books/stats")
def get_statistics():
    total_sold_money = 0
    for book in book_list:
        total_sold_money = book['sold'] * book['price'] + total_sold_money
    
    return {
        "message" : "Thống kê sách",
        "profit" : total_sold_money,
        "total_books" : len(book_list)

    }



# BaseModel có 3 nhiệm vụ tối quan trọng sau:
# Định nghĩa "Bộ khung" dữ liệu (Schema): Bạn dùng nó để khai báo cho hệ thống biết một đối tượng (ví dụ: SanPham) bắt buộc phải có những thông tin gì (id, ten, gia) và mỗi thông tin thuộc kiểu dữ liệu nào (int, str, float).
# Tự động ép kiểu (Data Parsing): Nếu người dùng gửi lên chuỗi chữ "100" cho trường gia (vốn là kiểu số), BaseModel sẽ thông minh tự động đổi nó thành số 100.0 cho bạn xử lý.
# Tự động chuyển đổi dạng dữ liệu (Serialization): Nó cung cấp hàm .model_dump() giúp bạn biến một đối tượng phức tạp thành một JSON/Dictionary thuần túy của Python chỉ trong một dòng code để lưu vào database.