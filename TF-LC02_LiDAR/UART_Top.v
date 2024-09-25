module UART_TOP(
	input i_Clk,
	input i_Rst,

	input i_Rx,
	output o_Tx,

	input start,
	output [6:0] o_FND0,
	output [6:0] o_FND1,
	output [6:0] o_FND2,
	output [6:0] o_FND3,
	output [1:0] debug_state


	);


wire			Tx_i_fTx;
wire	[7:0]	Tx_i_Data;

wire			Tx_o_fDone;
wire			Tx_o_fReady;

wire			Rx_o_fDone;
wire	[7:0]	Rx_o_Data;

reg [15:0] distance;
reg [63:0] c_Rx_Data, n_Rx_Data;
reg [39:0] c_Tx_Data, n_Tx_Data;
reg Tx_fStart;

reg [3:0] c_ByteCnt, n_ByteCnt;

UART_TX	TXD0(i_Clk, i_Rst, Tx_i_fTx,	Tx_i_Data,	Tx_o_fDone, Tx_o_fReady,	o_Tx);
UART_RX	RXD0(i_Clk, i_Rst,				i_Rx, 		Rx_o_fDone, Rx_o_Data);

// FND U0(distance%10 		 	, o_FND0);
// FND U1((distance/10) %10 	, o_FND1);
// FND U2((distance/100) %10 	, o_FND2);
// FND U3((distance/1000) %10 	, o_FND3);


/*
	Tx cmd first, receive data later
	send data : 55 AA 81 00 FA 	(5 byte) --> 10011001 10101010 10000001 00000000 11111010
	receive data(ex) : 55 AA 81 03 01 55 00 FA (8 byte)
*/

parameter 	IDLE = 2'd0,
			TX_DATA = 2'd1,
			RX_DATA = 2'd2,
			DONE = 2'd3;


reg [1:0] c_State, n_State;

assign Tx_i_fTx = Tx_fStart;
assign Tx_i_Data = c_Tx_Data[39:32];

always@(posedge i_Clk, negedge i_Rst)
	if(!i_Rst) begin
		c_State <= 0;
		c_Tx_Data <= 0;
		c_Rx_Data <= 0;
		c_ByteCnt <= 0;
	end else begin
		c_State <= n_State;
		c_Tx_Data <= n_Tx_Data;
		c_Rx_Data <= n_Rx_Data;
		c_ByteCnt <= n_ByteCnt;
	end



always@* begin
	n_Tx_Data <= c_Tx_Data;
	Tx_fStart <= 0;
	n_ByteCnt <= c_ByteCnt;
	n_State <= c_State;
	n_Rx_Data <= c_Rx_Data;

	case(c_State)
		IDLE : begin 
			n_Tx_Data <= 40'h55AA8100FA;
			if(start) n_State <= TX_DATA;
		end

		TX_DATA : begin
			// send 55 AA 81 00 FA
			if(Tx_o_fReady) begin 
				n_Tx_Data <= {c_Tx_Data[31:0], 8'h0};
				Tx_fStart <= 1;
				n_ByteCnt <= c_ByteCnt + 1;
			end

			if(c_ByteCnt == 5) begin // after sending FA
				n_State <= RX_DATA;
				n_ByteCnt <= 0;
			end
		end

		RX_DATA : begin
			// receive 55 AA 81 03 01 55 00 FA (example)
			if(Rx_o_fDone)
				begin
					n_Rx_Data <= {c_Rx_Data[55:0], Rx_o_Data};
					n_ByteCnt <= c_ByteCnt + 1;
				end
			if(c_ByteCnt == 8) n_State <= IDLE;
			// if(Rx_o_Data == 8'hFA) n_State <= IDLE;
				
		end

		// DONE : begin
		// // Result comes out with unsigned value
		// 		distance <= c_Rx_Data[31:28] * 16**3 + c_Rx_Data[27:24] * 16**2 + c_Rx_Data[23:20] * 16**1 + c_Rx_Data[19:16];
		// 		// distance % 10, distance % 100, distance % 1000
		// 		n_State <= IDLE;
		// end
	endcase
end

// wire distance_error;
// assign distance_error = !(c_State == DONE && c_Rx_Data[15:8] == 16'h00);

assign debug_state = c_State;

endmodule



module tb_uart();

reg i_Clk, i_Rst, i_Rx;
wire o_Tx;
reg start;

UART_TOP U0(
	i_Clk,
	i_Rst,
	i_Rx,
	o_Tx,
	start,
	,
	,
	
	,

);

always 
#10 i_Clk = ~i_Clk;

initial
begin
	i_Clk = 0; i_Rst = 0; start = 0; i_Rx = 0;
	@(negedge i_Clk) i_Rst = 1;
	#100 start = 1;
	#40 start = 0;

end
endmodule