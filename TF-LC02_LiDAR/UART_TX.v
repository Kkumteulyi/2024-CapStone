module UART_TX(i_Clk, i_Rst, 
	i_fTx, i_Data, o_fDone, o_fReady, o_Tx);
    
parameter	BAUD	= 115200;
parameter	CLK_FREQ= 50_000_000;
parameter	CYCLES_PER_BIT	= CLK_FREQ / BAUD;

input	i_Clk;
input	i_Rst;
input	i_fTx;
input	[ 7:0]	i_Data;		// 1 byte to transmit
output	wire	o_fDone;	// when transmition is o_fDone
output	wire	o_fReady;	// when there is no data to transmit
output	wire	o_Tx;		// uart txd signal

/* register */
reg		[1:0]	c_State,	n_State;
reg		[8:0]	c_ClkCnt,	n_ClkCnt;		// input i_Clk -> baud rate
reg		[2:0]	c_BitCnt,	n_BitCnt;		// counting the data bit(0 ~ 7)
reg		[8:0]	c_Data,		n_Data;

wire	fIdle,		fTxData,	fTxStop;	// flag for State
wire	fLstClk,	fLstBit;
wire	fIncClkCnt;

parameter	IDLE	= 2'h0;	// o_Tx = 1
parameter	TX_START= 2'h1;	// o_Tx = 0;
parameter	TX_DATA	= 2'h2;	// o_Tx = data bit
parameter	TX_STOP	= 2'h3;	// o_Tx = 1;

assign	o_fReady= fIdle;
assign	o_fDone	= fTxStop && fLstClk;
assign	o_Tx	= c_Data[0];

always@(posedge i_Clk, negedge i_Rst)
	if(!i_Rst) begin
		c_State		= IDLE;
		c_ClkCnt	= 0;
		c_BitCnt	= 0;
		c_Data		= 9'h1ff;
	end	else begin
		c_ClkCnt	= n_ClkCnt;
		c_State		= n_State;
		c_BitCnt	= n_BitCnt;
		c_Data		= n_Data;
	end

assign	fIdle		= c_State == IDLE,
		fTxData		= c_State == TX_DATA,
		fTxStop		= c_State == TX_STOP;
assign	fLstClk		= c_ClkCnt == CYCLES_PER_BIT,
		fLstBit		= fLstClk && &c_BitCnt;
assign	fIncClkCnt	= !fIdle  && !fLstClk;

always@* begin
	n_Data		= fIdle && i_fTx	? {i_Data, 1'b0}: fLstClk ? {1'b1, c_Data[8:1]} : c_Data;
	n_ClkCnt	= fIncClkCnt		? c_ClkCnt + 1	: 0;
	n_BitCnt	= fTxData	? fLstClk ? c_BitCnt +1 : c_BitCnt : 0;

	n_State		= c_State;
	case(c_State)
		IDLE	:	if(i_fTx)	n_State	= TX_START;
		TX_START:	if(fLstClk)	n_State = TX_DATA;
		TX_DATA:	if(fLstBit)	n_State = TX_STOP;
		default	:	if(fLstClk)	n_State	= IDLE;
	endcase
end

endmodule
