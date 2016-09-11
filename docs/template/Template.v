`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 09/11/2016 09:28:57 AM
// Design Name: 
// Module Name: Template
// Project Name: 
// Target Devices: 
// Tool Versions: 
// Description: 
// 
// Dependencies: 
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
//////////////////////////////////////////////////////////////////////////////////
module Template(
    input wire clk,
    input wire rst_n,
    
    input wire uart_rx,
    output wire uart_tx,
    
    input wire [4:1] sw,
    input wire [4:1] btn
);

    GpioWrapper wrapper (
        .clk(clk),
        .rst_n(rst_n),
        
        .uart_rx(uart_rx),
        .uart_tx(uart_tx),
        
        .segs({8{sw[4:1]}}),
        .led({4{btn[4:1]}})
    );

endmodule
