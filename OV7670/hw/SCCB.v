module SCCB 
#(
	parameter SCCB_F = 100_000, 		// SCCB bus frequency = 100Khz
	// parameter DEV_F = 50_000_000 	// Device frequency = 50Mhz
	parameter DEV_F = 500_000 // for simulation
)( 
	input i_Clk, 
	input i_Rst,
	input [7:0] i_Addr,
	input [7:0] i_Data,
	input i_fStart,

	output o_fReady,
	output o_SIO_C,
	output o_SIO_D


	);

localparam BUS_WAIT_FOR_SYNC_CYCLE = DEV_F / SCCB_F - 1; 	// SCCB bus's 1 clock
parameter CAMERA_ADDR = 8'h42;
parameter IDLE = 0;
parameter START_1 = 1;
parameter START_2 = 2;
parameter TX_1 = 3;
parameter TX_2 = 4;
parameter TX_3 = 5;
parameter TX_4 = 6;
parameter END_1 = 7;
parameter END_2 = 8;
parameter END_3 = 9;
parameter END_4 = 10;
parameter DONE = 11;

reg c_SIO_C, n_SIO_C;
reg	c_SIO_D, n_SIO_D;
reg [8:0] c_timer, n_timer; // 500 cycle
reg [3:0] c_State, n_State;
reg [3:0] c_ByteIdx, n_ByteIdx;
reg [1:0] c_ByteCnt, n_ByteCnt;
reg [7:0] c_TX_Byte, n_TX_Byte;


always@(posedge i_Clk, negedge i_Rst)
	if(!i_Rst) begin
		c_State <= 0;
		c_SIO_C <= 0;
		c_SIO_D <= 0;
		c_timer <= 0;
		c_ByteIdx <= 0;
		c_ByteCnt <= 0;
		c_TX_Byte <= 0;
	end else begin
		c_State <= n_State;
		c_SIO_C <= n_SIO_C;
		c_SIO_D <= n_SIO_D;
		c_timer <= n_timer;
		c_ByteIdx <= n_ByteIdx;
		c_ByteCnt <= n_ByteCnt;
		c_TX_Byte <= n_TX_Byte;
	end



reg [7:0] r_latch_addr;
reg [7:0] r_latch_data;
reg r_Ready;



// 8bit send
always@* begin
	n_State <= c_State;
	n_SIO_C <= c_SIO_C;
	n_SIO_D <= c_SIO_D;
	n_timer <= c_timer;
	n_ByteIdx <= c_ByteIdx;
	n_ByteCnt <= c_ByteCnt;
	n_TX_Byte <= c_TX_Byte;
	case(c_State)
		IDLE: begin
			n_ByteIdx <= 0;
			n_ByteCnt <= 0;
			r_Ready <= 1;
			n_timer <= 0;
			if(i_fStart)	// SCCB interface start, put value to bus
				begin
					r_latch_addr <= i_Addr;
					r_latch_data <= i_Data;
					r_Ready <= 0;
					n_State <= START_1;
				end
		end
		START_1: begin
			n_SIO_C <= 0;
			n_SIO_D <= 1;
			n_timer <= c_timer + 1;
			if(c_timer == BUS_WAIT_FOR_SYNC_CYCLE) begin // SCCB bus 1 clock 
				n_State <= START_2;
				n_timer <= 0; // bus clock counter reset
			end
		end

		START_2: begin
			// select transmit bits or end protocol
			n_State <= c_ByteCnt == 3 ? END_1 : TX_1;
			n_ByteCnt <= c_ByteCnt + 1;
			n_ByteIdx <= 0;
			case(c_ByteCnt)
				0: n_TX_Byte <= CAMERA_ADDR; // Camera I2C Address (3-wire)
				1: n_TX_Byte <= r_latch_addr;
				2: n_TX_Byte <= r_latch_data;
				default: n_TX_Byte <= r_latch_data;
			endcase
		end

/*
	TX data phase
*/
		TX_1: begin
			n_SIO_C <= 1;
			n_timer <= c_timer + 1;
			if(c_timer == BUS_WAIT_FOR_SYNC_CYCLE) begin // SCCB bus 1 clock
				n_State <= TX_2;
				n_timer <= 0;
			end
		end

		TX_2: begin
			n_timer <= c_timer + 1;
			n_SIO_D <= (c_ByteIdx == 8) ? 0 : ~c_TX_Byte[7]; 	// I2C 의 반대로 동작
			if(c_timer == BUS_WAIT_FOR_SYNC_CYCLE) begin 
				n_State <= TX_3;
				n_timer <= 0;
			end
		end

		TX_3: begin
			n_timer <= c_timer + 1;
			n_SIO_C <= 0;
			if(c_timer == BUS_WAIT_FOR_SYNC_CYCLE) begin 
				n_State <= TX_4;
				n_timer <= 0;
			end
		end

		TX_4: begin
			n_State <= c_ByteIdx == 8 ? START_2 : TX_1;
			n_TX_Byte <= {c_TX_Byte[6:0], 1'b0}; // TX Byte << 1
			n_ByteIdx <= c_ByteIdx + 1; 	// 타이밍이 이상함
		end

/*
	End Communication Phase
*/
		END_1: begin
			n_SIO_C <= 1;
			n_timer <= c_timer + 1;
			if(c_timer == BUS_WAIT_FOR_SYNC_CYCLE) begin 
				n_State <= END_2;
				n_timer <= 0;
			end
		end

		END_2: begin
			n_SIO_D <= 1;
			n_timer <= c_timer + 1;
			if(c_timer == BUS_WAIT_FOR_SYNC_CYCLE) begin 
				n_State <= END_3;
				n_timer <= 0;
			end
		end

		END_3: begin
			n_SIO_C <= 0;
			n_timer <= c_timer + 1;
			if(c_timer == BUS_WAIT_FOR_SYNC_CYCLE) begin 
				n_State <= END_4;
				n_timer <= 0;
			end
		end

		END_4: begin
			n_SIO_D <= 0;
			n_timer <= c_timer + 1;
			if(c_timer == BUS_WAIT_FOR_SYNC_CYCLE) begin 
				n_State <= DONE;
				n_timer <= 0;
			end
		end

		DONE: begin
			n_timer <= c_timer + 1;
			if(c_timer == BUS_WAIT_FOR_SYNC_CYCLE) begin 
				n_State <= IDLE;
				n_timer <= 0;
			end
		end
	endcase
end

assign 	o_fReady = r_Ready;
assign 	o_SIO_C = c_SIO_C,
		o_SIO_D = c_SIO_D;


endmodule


module test_SCCB();

reg i_Clk;
reg i_Rst;
reg [7:0] i_Addr;
reg [7:0] i_Data;
reg i_fStart;

wire o_fReady;
wire o_SIO_C;
wire o_SIO_D;

SCCB SCCB
( 
	i_Clk, 
	i_Rst,
	i_Addr,
	i_Data,
	i_fStart,

	o_fReady,
	o_SIO_C,
	o_SIO_D
	);

always
	#10 i_Clk = ~i_Clk;

initial
begin
	i_Clk = 0; i_Rst = 0;
	i_Addr = 8'h11; i_Data = 8'h22;
	i_fStart = 0;
	@(negedge i_Clk) i_Rst = 1;
	@(negedge i_Clk) i_fStart = 1;
	#20 i_fStart = 0;

end
endmodule




// 어딘가에서 무한 반복 중