module convolution
	#(
		// Through this convolution block, input data size becomes half.
		parameter 	IN_WIDTH = 64, 
					IN_HEIGHT = 64, 
					IN_CHANNEL = 3,
					FILTER_SIZE = 3, 
					STRIDE = 2, 
					PADDING = 1,
					OUT_CHANNEL = 16 		// same size w. bias, gamma, beta 
	)
	( 				
	input i_Clk,
	input i_Rst,





	);
// Define OUT Parameter 
parameter OUT_HEIGHT = (IN_HEIGHT - FILTER_SIZE + 2 * PADDING) / STRIDE + 1;
parameter OUT_WIDTH = (IN_WIDTH - FILTER_SIZE + 2 * PADDING) / STRIDE + 1;







// receiving continous data 
conv2d conv_layer();



// if conv2d done
batchnorm batch_norm_layer();



// if batchnorm done
silu activation_silu();


// output data : (OUT_CHANNEL, IN_HEIGHT/2, IN_WIDTH/2)

endmodule



