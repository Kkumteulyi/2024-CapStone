/* 

Author : Yunhyeok Jeong
Date : Apr. 15 2024
OV7670 Camera module

OV7670 supports 30fps for VGA(640*480)

image array (656 * 488)

REF : https://www.voti.nl/docs/OV7670.pdf

*/

module Camera(  
    // SCL, SDA
    output o_SCL,
    inout o_SDA,       //SDA, use this when control slave options

    // Data[7:0]
    input [7:0] i_Data,

    // MCLK(System clock)
    output o_MCLK,

    // VSYNC, HREF, Pixel Clock
    input i_VSYNC,
    input i_HREF,
    input i_PCLK,

    // Reset, Power Down
    output o_Rst,    
    output o_PWDN      //0: Normal mode, 1: Power down mode 
    
);

/*

SCCB Timing Diagram

(1) T(su:sta) min 100 ns
(2) T(hd:sta) min 600 ns
(3) T(F) max 300 ns
(4) T(low) min 1.3 us
(5) T(high) min 600 ns
(6) T(hd:dat) can run immediately
(7) T(su:dat) min 100 ns
(8) T(r) max 300 ns
(9) T(su:sto) min 600 ns
(10) T(buf) min 1.3 us

(11) T(aa) SCL low to Data out validm min 100ns ~ max 900ns
(12) T(dh) Data-out hold time, min 50ns

*/

/*

Horizontal Timing
(1) T(pclk) : For raw data, T(p) == T(pclk) / For YUV/RGB, T(p) == 2 * T(pclk)
(2) T(phl) : neg PCLK to neg HREF, min 0 ns to max 5 ns
(3) T(pdv) : neg PCLK to Data-out valid, max 5ns
(4) T(su) : D[7:0] Setup time, min 15ns
(5) T(hd) : D[7:0] Hold time, min 8ns


*/

/*

VGA Frame Timing
t(LINE) : 784t(p)
t(p) : For raw data, t(p) = t(PCLK) | For YUV/RGB, t(p) = 2 * t(PCLK)
t(p) : pixel clock, generally 1 clock, so t(LINE) takes 784 clocks(RAW data)
VSYNC : 510 * t(LINE) = 510 * 784t(p)

and 1 cycle of VSYNC (include row 0 to 479)
total takes 784 * 510 = 399,840 clocks

and typical boards got 50Mhz clock speed, 1 clock takes 20ns
399,840 clocks takes 7,996,800ns (convert to ms, 7.996800ms)
8ms for 1 frame

spec 30fps needs about 33 ms per frame

?

divide clocks, 50Mhz to 12.5Mhz
then 1 clock takes 80ns
399,840 clocks takes 31,987,200ns (convert to ms, 31.987200ms)
32ms for 1 frame
about 31.25 fps

and
Not a RAW data, YUV/RGB
t(p) should be 2x
so divide clocks, 50Mhz to 25Mhz
(Need double data blocks)
then 1 clock takes 80ns. 

t(LINE) : 784t(p) (t(p) = 2*t(PCLK), 1568t(p))
VSYNC : 510 * t(LINE) = 510 * 1568t(p)

*/


