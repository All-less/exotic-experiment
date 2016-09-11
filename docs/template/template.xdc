set_property -dict {LOC AC18 IOSTANDARD LVCMOS18} [get_ports clk]
create_clock -period 10.000 -name clk_i -waveform {0.000 5.000} clk
set_property -dict {LOC W13 IOSTANDARD LVCMOS18} [get_ports rst_n]

set_property -dict {LOC W26  IOSTANDARD LVCMOS33} [get_ports btn[1]]
set_property -dict {LOC V21  IOSTANDARD LVCMOS33} [get_ports btn[2]]
set_property -dict {LOC W21  IOSTANDARD LVCMOS33} [get_ports btn[3]]
set_property -dict {LOC AA25 IOSTANDARD LVCMOS33} [get_ports btn[4]]
set_property -dict {LOC AB25 IOSTANDARD LVCMOS33} [get_ports sw[1]]
set_property -dict {LOC W23  IOSTANDARD LVCMOS33} [get_ports sw[2]]
set_property -dict {LOC W24  IOSTANDARD LVCMOS33} [get_ports sw[3]]
set_property -dict {LOC AB26 IOSTANDARD LVCMOS33} [get_ports sw[4]]

set_property -dict {LOC L25 IOSTANDARD LVCMOS33 SLEW FAST PULLUP true} [get_ports uart_rx]
set_property -dict {LOC P24 IOSTANDARD LVCMOS33 SLEW FAST DRIVE 16 PULLUP true} [get_ports uart_tx]