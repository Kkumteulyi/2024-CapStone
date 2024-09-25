module FND(i_Data, o_FND);
	
input	[3:0] i_Data;
output	reg	[6:0] o_FND;	// fnd data setting : g~a

always@*
	case(i_Data)
		4'h0	: o_FND = 7'b1000000;
		4'h1	: o_FND = 7'b1111001;
		4'h2	: o_FND = 7'b0100100;
		4'h3	: o_FND = 7'b0110000;
		4'h4	: o_FND = 7'b0011001;
		4'h5	: o_FND = 7'b0010010;
		4'h6	: o_FND = 7'b0000010;
		4'h7	: o_FND = 7'b1011000;
		4'h8	: o_FND = 7'b0000000;
		4'h9	: o_FND = 7'b0011000;
		4'ha	: o_FND = 7'b0001000;
		4'hb	: o_FND = 7'b0000011;
		4'hc	: o_FND = 7'b0100111;
		4'hd	: o_FND = 7'b0100001;
		4'he	: o_FND = 7'b0000110;
		default	: o_FND = 7'b0001110;
	endcase
	
endmodule
