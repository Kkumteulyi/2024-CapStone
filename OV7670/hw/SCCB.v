module SCCB(
	input i_Clk,
	input i_Rst,
	input i_fStart,
	input [7:0] i_Addr,
	input [7:0] i_Data,
	output o_fReady,
	output reg o_SIO_C,
	output reg o_SIO_D
	);

localparam SCCB_FREQ = 100_000 // SCCB interface frequency, 100 Khz
localparam DEV_FREQ = 50_000_000 // Device frequency, 50Mhz


assign o_fReady = c_State == IDLE; // if c_state == idle, then o_Ready == 1 or 0


always@(posedge i_Clk, negedge i_Rst) 
	if(!i_Rst) begin
		c_State <= 0;
	end else begin
		c_State <= n_State;
	end


reg [7:0] r_Saved_Data;
reg [7:0] r_Saved_Addr;
reg [] r_BCnt; // Byte Counter
reg [] r_BIdx; // Byte Index


always@* begin
	n_State <= c_State;
	case(c_State)
		IDLE : begin 
			r_Saved_Addr <= 0;
			r_Saved_Data <= 0;
			r_BCnt <= 0;
			r_BIdx <= 0;

			if(i_fStart) begin
				r_Saved_Addr <= i_Addr;
				r_Saved_Data <= i_Data;
				n_State <= ; // to start sccb interface
			end
		end

		START_BUS : begin
			


		end


end