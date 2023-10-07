import copy

class State:
    def __init__(self, Matrix = None): # Khởi tạo lớp State với tham số Matrix mặc định là None
        self.Matrix = Matrix # Gán giá trị Matrix cho thuộc tính Matrix của lớp

    def Clone(self): # Phương thức sao chép đối tượng State
        return copy.deepcopy(self) # Sử dụng phương thức deepcopy của module copy để sao chép đối tượng

    def Print(self): # Phương thức in ra trạng thái hiện tại của bảng game
        for I, Row in enumerate(self.Matrix): # Duyệt qua từng hàng của ma trận
            for J, Element in enumerate(Row): # Duyệt qua từng phần tử trong hàng
                if Element == 0: # Nếu phần tử bằng 0, in ra "-"
                    print("-",end=' ')
                elif Element == 1: # Nếu phần tử bằng 1, in ra "O"
                    print("O",end=' ')
                else: # Nếu phần tử khác 0 và 1, in ra "X"
                    print("X",end=' ')
            print() # Xuống dòng sau khi in xong một hàng
        print() # Xuống dòng sau khi in xong toàn bộ ma trận

    def Is_End_Node(self): # Kiểm tra xem trạng thái hiện tại có phải là trạng thái kết thúc không (không còn nước đi nào nữa)
        for I, Row in enumerate(self.Matrix): # Duyệt qua từng hàng của ma trận
            for J, Element in enumerate(Row): # Duyệt qua từng phần tử trong hàng
                if Element == 0: # Nếu có phần tử bằng 0 (còn nước đi), trả về False
                    return False
        return True # Nếu không có phần tử nào bằng 0 (không còn nước đi), trả về True

    def Win_State(self): # Kiểm tra xem trạng thái hiện tại có phải là trạng thái chiến thắng không (3 quân cùng loại nằm trên một hàng, cột hoặc đường chéo)
        M = self.Matrix # Gán ma trận hiện tại vào biến M để tiện xử lý
        if M == None: # Nếu ma trận rỗng, trả về False
            return False
        for i in range(3): # Kiểm tra các hàng
            if M[i][0] != 0 and M[i][0] == M[i][1] and M[i][0] == M[i][2]:
                return True
        for j in range(3): # Kiểm tra các cột
            if M[0][j] != 0 and M[0][j] == M[1][j] and M[0][j] == M[2][j]:
                return True
        if M[0][0] != 0 and M[0][0] == M[1][1] and M[0][0] == M[2][2]: # Kiểm tra đường chéo từ trái sang phải
            return True
        if M[0][2] != 0 and M[0][2] == M[1][1] and M[0][2] == M[2][0]: # Kiểm tra đường chéo từ phải sang trái
            return True

    def Check_My_Turn(self): # Kiểm tra xem có phải lượt của mình không (dựa vào số lượng ô đã được đi - nếu là số chẵn thì là lượt của mình)
        Res = 0
        for I, Row in enumerate(self.Matrix):
            for J, Element in enumerate(Row):
                if Element != 0:
                    Res += 1
        if Res % 2 == 0:
            return True
        return False

    def Value(self): # Đánh giá giá trị của trạng thái (1 nếu thắng, -1 nếu thua, 0 nếu hòa hoặc chưa kết thúc)
        if self.Win_State():
            if self.Check_My_Turn():
                return 1
            return -1
        return 0


class Operator:
    def __init__(self, x = 0, y = 0): # Khởi tạo lớp Operator với tham số x, y mặc định là 0
        self.x = x # Gán giá trị x cho thuộc tính x của lớp
        self.y = y # Gán giá trị y cho thuộc tính y của lớp

    def Move(self, State): # Phương thức di chuyển trên bảng game
        if self.x < 0 or self.x >= 3: # Kiểm tra xem tọa độ x có nằm ngoài bảng game không
            return None
        if self.y < 0 or self.y >= 3: # Kiểm tra xem tọa độ y có nằm ngoài bảng game không
            return None
        if State.Matrix[self.x][self.y] != 0: # Kiểm tra xem ô tại tọa độ (x, y) đã được đi chưa
            return None
        Res = 0
        for I, Row in enumerate(State.Matrix):
            for J, Element in enumerate(Row):
                if Element != 0:
                    Res += 1
        Copy = State.Clone() # Tạo một bản sao của trạng thái hiện tại
        if Res % 2 == 0: # Nếu số lượng ô đã được đi là số chẵn (lượt của người chơi 1)
            Copy.Matrix[self.x][self.y] = 1 # Đánh dấu ô tại tọa độ (x, y) là của người chơi 1
        else: # Nếu số lượng ô đã được đi là số lẻ (lượt của người chơi 2)
            Copy.Matrix[self.x][self.y] = 2 # Đánh dấu ô tại tọa độ (x, y) là của người chơi 2
        return Copy

def Alpha_Beta(State, Depth, Alpha, Beta, Max_Min_Player): # Hàm Alpha-Beta Pruning để tìm nước đi tối ưu
    if State.Is_End_Node() or Depth == 0: # Nếu trạng thái hiện tại là trạng thái kết thúc hoặc đã duyệt đủ chiều sâu
        return State.Value() # Trả về giá trị của trạng thái
    if Max_Min_Player == True: # Nếu là người chơi Max (người chơi 1)
        for i in range(3):
            for j in range(3):
                Child = Operator(i, j).Move(State) # Tạo ra một trạng thái con từ nước đi (i, j)
                if Child == None: # Nếu nước đi (i, j) không hợp lệ, bỏ qua và tiếp tục vòng lặp
                    continue
                Temp = Alpha_Beta(Child, Depth-1, Alpha, Beta, False) # Gọi đệ quy hàm Alpha-Beta Pruning cho trạng thái con
                Alpha = max(Alpha, Temp) # Cập nhật giá trị Alpha
                if Alpha > Beta: # Nếu Alpha > Beta, cắt tỉa nhánh hiện tại và dừng vòng lặp
                    break
        return Alpha # Trả về giá trị Alpha (giá trị tối đa mà người chơi Max có thể đạt được)
    else: # Nếu là người chơi Min (người chơi 2)
        for i in range(3):
            for j in range(3):
                Child = Operator(i, j).Move(State) # Tạo ra một trạng thái con từ nước đi (i, j)
                if Child == None: # Nếu nước đi (i, j) không hợp lệ, bỏ qua và tiếp tục vòng lặp
                    continue
                Temp = Alpha_Beta(Child, Depth-1, Alpha, Beta, True) # Gọi đệ quy hàm Alpha-Beta Pruning cho trạng thái con
                Beta = min(Beta, Temp) # Cập nhật giá trị Beta
                if Alpha >= Beta: # Nếu Alpha >= Beta, cắt tỉa nhánh hiện tại và dừng vòng lặp
                    break
        return Beta # Trả về giá trị Beta (giá trị tối thiểu mà người chơi Min có thể đạt được)


def Tic_Tac_Toe_Game(): # Hàm chính để chơi trò Tic Tac Toe
    Player = 1 # Khởi tạo người chơi là 1
    Turn = 0 # Khởi tạo lượt chơi là 0
    S = State([[0,0,0],[0,0,0],[0,0,0]]) # Khởi tạo trạng thái ban đầu của bảng game
    S.Print() # In ra trạng thái ban đầu của bảng game
    while True: # Bắt đầu vòng lặp game
        if Turn % 2 + 1 == Player: # Nếu là lượt của người chơi
            Child = None
            while Child == None: # Yêu cầu người chơi nhập vào nước đi cho đến khi nước đi hợp lệ
                print("Nhập vào tọa độ:")
                x = int(input("x = ")) # Nhập vào tọa độ x
                y = int(input("y = ")) # Nhập vào tọa độ y
                Child = Operator(x,y).Move(S) # Tạo ra trạng thái con từ nước đi (x, y)
            S = Child # Cập nhật trạng thái hiện tại sau khi người chơi đi
            if S.Win_State(): # Kiểm tra xem người chơi có thắng không
                S.Print() # In ra trạng thái hiện tại của bảng game
                print("Nguời chơi thắng") # Thông báo người chơi thắng
                break # Kết thúc game
        else: # Nếu là lượt của máy
            AI = 2
            Min_Child = None
            for i in range(3):
                for j in range(3):
                    Child = Operator(i, j).Move(S) # Tạo ra một trạng thái con từ nước đi (i, j)
                    if Child == None: # Nếu nước đi (i, j) không hợp lệ, bỏ qua và tiếp tục vòng lặp
                        continue
                    Temp = Alpha_Beta(Child, 1, -2, 2, True) # Gọi hàm Alpha-Beta Pruning để tìm nước đi tối ưu cho máy
                    if AI > Temp:
                        AI = Temp
                        Min_Child = Child
            S = Min_Child # Cập nhật trạng thái hiện tại sau khi máy đi
            if S.Win_State(): # Kiểm tra xem máy có thắng không
                S.Print() # In ra trạng thái hiện tại của bảng game
                print("Người chơi thua") # Thông báo người chơi thua
                break # Kết thúc game
        S.Print() # In ra trạng thái hiện tại của bảng game sau mỗi lượt đi
        if S.Is_End_Node(): # Kiểm tra xem đã hết nước đi không (trò chơi kết thúc)
            print("Người và máy hòa nhau") # Thông báo kết quả hòa nếu không còn nước đi nào nữa
            break # Kết thúc game
        Turn += 1 # Tăng số lượng lượt đi lên 1 sau mỗi lượt đi của người chơi và máy
Tic_Tac_Toe_Game()