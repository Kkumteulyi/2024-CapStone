module UART_RX(i_Clk, i_Rst, 
	i_Rx, o_fDone, o_Data);

parameter	BAUD	= 115200;
parameter	CLK_FREQ= 50_000_000;
parameter	CYCLES_PER_BIT	= CLK_FREQ / BAUD;

input	i_Clk;
input	i_Rst;
input	i_Rx;						// uart rxd signal
output	wire			o_fDone;	// when there is received data
output	wire	[7:0]	o_Data;		// received byte 

/* register */
reg		[1:0]	c_State,	n_State;
reg		[8:0]	c_ClkCnt,	n_ClkCnt;		// input i_Clk -> baud rate
reg		[2:0]	c_BitCnt,	n_BitCnt;		// counting the data bit(0 ~ 7)
reg		[7:0]	c_Data,		n_Data;			// current ceceived data
reg				c_Rx,		n_Rx;

wire	fRxData;	// flag for State
wire	fLstClk,	fLstBit,	fCapture;
wire	fIncClkCnt,	fCaptureData;

parameter	IDLE	= 2'h0;	// i_Rx = 1
parameter	RX_START= 2'h1;	// i_Rx = 0;
parameter	RX_DATA	= 2'h2;	// i_Rx = data bit
parameter	RX_STOP	= 2'h3;	// i_Rx = 1;

assign	o_fDone	= c_State == RX_STOP;
assign	o_Data	= o_fDone ? c_Data : 0;

always@(posedge i_Clk, negedge i_Rst)
	if(!i_Rst)	begin
		c_State		= IDLE;
		c_ClkCnt	= 0;
		c_BitCnt	= 0;
		c_Data		= 0;
		c_Rx		= 1;
	end	else begin
		c_ClkCnt	= n_ClkCnt;
		c_State		= n_State;
		c_BitCnt	= n_BitCnt;
		c_Data		= n_Data;
		c_Rx		= n_Rx;
	end

assign	fRxData		= c_State == RX_DATA;
assign	fCapture	= c_ClkCnt == CYCLES_PER_BIT / 2,	// time to check i_Rx
		fLstClk		= c_ClkCnt == CYCLES_PER_BIT,
		fLstBit		= fLstClk && &c_BitCnt;
assign	fIncClkCnt	= ^c_State && !fLstClk,
		fCaptureData= fCapture && fRxData;

always@* begin
	n_Rx		= i_Rx;
	n_Data		= fCaptureData	? {c_Rx, c_Data[7:1]}	: c_Data;
	n_ClkCnt	= fIncClkCnt	? c_ClkCnt + 1			: 0;
	n_BitCnt	= fRxData		? fLstClk ? c_BitCnt+1	: c_BitCnt : 0;

	n_State		= c_State;
	case(c_State)
		IDLE	:	if(!c_Rx)				n_State	= RX_START;
		RX_START:	if(fCapture && c_Rx)	n_State = IDLE;			// ERROR
					else if(fLstClk)		n_State = RX_DATA;
		RX_DATA	:	if(fLstBit)				n_State = RX_STOP;
		RX_STOP	:							n_State = IDLE;
	endcase
end

endmodule
