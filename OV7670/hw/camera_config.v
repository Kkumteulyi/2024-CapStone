/*
	이 모듈의 역할은 camera_init flag 들을 가져와서 
	SCCB interface 로 보내주는 역할
	따라서 reset 되거나 최초 시작시 1회만 동작하게 됨.

*/

module camera_config(
	input i_Clk,
	input i_Rst,

	input i_SCCB_fReady,
	output i_SCCB_fStart,

	output o_1b_SCCB_Address,
	output o_1b_SCCB_Value
	);





wire [7:0] SCCB_Address;
wire [7:0] SCCB_Value;
/* 
posedge clk 에 따라서 데이터를 가져옴.
count(max 75, 7 bits) 값을 넣어서 지속적으로 값을 뽑고, 
나온 값을 8b / 8b 나눠서 sccb_address, sccb_value 로 분류
*/
camera_init init_reg(
.i_Clk(i_Clk),
.i_Rst(i_Rst),
.i_Addr(c_Cnt),
.o_Data({SCCB_Address, SCCB_Value})
);



reg [6:0] c_Cnt, n_Cnt;
reg c_State, n_State;

always@(posedge i_Clk, negedge i_Rst) 
	if(!i_Rst) begin
		c_Cnt <= 0;
		c_State <= 0;
	end else begin
		c_Cnt <= n_Cnt;
		c_State <= n_State;
	end


/* 만약 SCCB interface 가 현재 준비된 상태라면 
동작을 시킴. camera config 에서 보내 줄 값은 1 bit 씩 보내줘야 함. 따라서 bit counter 라는 것을 만듦.

*/
localparam IDLE = d'0;
localparam WORK = d'1;
localparam DONE = d'2;

reg [2:0] c_BCnt, n_BCnt;

always@* begin
	n_Cnt <= c_Cnt;
	n_State <= c_State;
	case(c_State)
		IDLE : if(i_SCCB_fReady)
			c_State <= WORK;

		WORK : 


		DONE : // n_Cnt <= c_Cnt + 1;

end