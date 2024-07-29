/*
	이 모듈의 역할은 camera_init flag 들을 가져와서 
	SCCB interface 로 보내주는 역할
	따라서 reset 되거나 최초 시작시 1회만 동작하게 됨.
*/

module camera_config(
	input i_Clk,
	input i_Rst,
	input i_Config_fStart, 	// 여기는 config start sign
	
	output o_SCCB_fReady,
	output o_1b_SCCB_Address,
	output o_1b_SCCB_Data,
	output reg o_init_flag_setting_done
	);

localparam IDLE = 0;
localparam WORK = 1;
localparam CHECK_COMM = 2;
localparam DONE = 3;

reg [7:0] c_Cnt, n_Cnt;	// counter range : 0~76(FFFF, end sign)
reg [1:0] c_State, n_State;
reg r_SCCB_fStart;

wire [7:0] SCCB_Address;
wire [7:0] SCCB_Value;
wire [15:0] SCCB_o_Data;

/* 
posedge clk 에 따라서 데이터를 가져옴.
count(max 75, 7 bits) 값을 넣어서 지속적으로 값을 뽑고, 
나온 값을 8b / 8b 나눠서 sccb_address, sccb_value 로 분류
*/
cam_rom init_reg(
.i_Clk(i_Clk),
.i_Rst(i_Rst),
.i_Addr(c_Cnt),
.o_Data(SCCB_o_Data)
);
assign SCCB_Address = SCCB_o_Data[15:8];
assign SCCB_Value = SCCB_o_Data[7:0];

SCCB SCCB_interface
( 
.i_Clk(i_Clk), 
.i_Rst(i_Rst),
.i_Addr(SCCB_Address), 	// 값을 넣을 레지스터 주소 (SCCB_Address)
.i_Data(SCCB_Value), 	// 넣을 값 (SCCB_Value)
.i_fStart(r_SCCB_fStart), 	// 버스 시작 사인
.o_fReady(o_SCCB_fReady), 	// 버스가 IDLE 상태인지 확인
.o_SIO_C(o_1b_SCCB_Address), 	// SCCB bus SCL 
.o_SIO_D(o_1b_SCCB_Data) 		// SCCB bus SDA
);



always@(posedge i_Clk, negedge i_Rst) 
	if(!i_Rst) begin
		c_Cnt <= 0;
		c_State <= 0;
		o_init_flag_setting_done <= 0;
	end else begin
		c_Cnt <= n_Cnt;
		c_State <= n_State;
		o_init_flag_setting_done <= (c_State == DONE) ? 1 : o_init_flag_setting_done; 	// camera 초기화가 완료되었다는 플래그
	end



always@* begin
	n_Cnt <= c_Cnt;
	n_State <= c_State;
	r_SCCB_fStart <= 0;
	case(c_State)
		IDLE : begin
			n_Cnt <= 0;
			if(i_Config_fStart) begin	// 기본적으로 o_fReady 가 활성화 되어 있을 때 Start sign 을 받아야 함
				n_State <= WORK;
				r_SCCB_fStart <= 1;
			end
		end

		WORK : begin
			if(o_SCCB_fReady) 	// SCCB 가 사용 가능할 때 까지 기다림.(통신이 끝날 때 까지 기다림)
				n_State <= CHECK_COMM;
		end

		CHECK_COMM: begin 	
			if(c_Cnt == 76)		// 통신 체크, 카운터가 76에 도달했는지
				n_State <= DONE; 	
			else begin
				n_State <= WORK;
				n_Cnt <= c_Cnt + 1;
				r_SCCB_fStart <= 1;
			end
		end

		DONE :	
			n_State <= IDLE; 	// 통신 종료
		
	endcase
end
endmodule


module tb_Camera_Top();

reg i_Clk;
reg i_Rst;
reg i_SCCB_fStart;
wire o_SCCB_fReady;
wire o_1b_SCCB_Address;
wire o_1b_SCCB_Data;
wire o_init_flag_setting_done;

camera_config cam(
.i_Clk(i_Clk),
.i_Rst(i_Rst),
.i_Config_fStart(i_SCCB_fStart),	
.o_SCCB_fReady(o_SCCB_fReady),
.o_1b_SCCB_Address(o_1b_SCCB_Address),
.o_1b_SCCB_Data(o_1b_SCCB_Data),
.o_init_flag_setting_done(o_init_flag_setting_done)
	);

always 
	#10 i_Clk = ~i_Clk;


initial
begin
	i_Clk = 0; i_Rst = 0; i_SCCB_fStart = 0;
	@(negedge i_Clk) i_Rst = 1;
	#20 i_SCCB_fStart = 1; 
	#20 i_SCCB_fStart = 0;
end
endmodule