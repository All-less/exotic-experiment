`timescale 1ns / 1ps

module GpioWrapper(
    input wire clk,
    input wire rst_n,
    
    input wire uart_rx,
    output wire uart_tx,
    
    input wire [31:0] segs,
    input wire [15:0] led
);

    wire rx_busy, 
         tx_busy, 
         rx_done, 
         tx_done;
    reg [7:0] data_in;
    wire [7:0] data_out;
    reg [47:0] data;
    
    localparam
        IDLE = 1,
        SENDING = 3,
        SENT = 4;
        
    reg [2:0] state = IDLE;
    reg [2:0] cnt = 0;
    reg we = 0;
    
    always @ (posedge clk) begin
        if (!rst_n) begin
            state <= IDLE;
            cnt <= 0;
        end else begin
            case(state)
                IDLE: begin
                    if (rx_done && data_out == 8'h1b) begin
                        state <= SENDING;
                        data <= {segs, led};
                    end
                end
                SENDING: begin
                    if (~tx_done) begin
                        data_in <= data[7:0];
                        data <= {8'b0, data[47:8]};
                        state <= SENT;
                        we <= 1'b1;
                    end
                end
                SENT: begin
                    if (tx_done) begin
                        if (cnt == 5) begin
                            state <= IDLE;
                            we <= 1'b0;
                            cnt <= 0;
                        end else begin
                            state <= SENDING;
                            cnt <= cnt + 1;
                        end
                    end
                end
            endcase
        end
    end
        
	Uart uart (
        .clk(clk),
        .rst(~rst_n),
        .rx(uart_rx),
        .tx(uart_tx),
        .we(we),
        .en(1'b1),
        .rx_busy(rx_busy),
        .tx_busy(tx_busy),
        .rx_done(rx_done),
        .tx_done(tx_done),
        .data_in(data_in),
        .data_out(data_out)
    );

endmodule