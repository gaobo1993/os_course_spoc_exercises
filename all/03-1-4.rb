
begin
    file = File.new("03-1-4-input.txt", "r")
    while (line = file.gets)
        words = line.split
        va, pa = words[1].hex, words[3].hex
        pde_idx = ((va & 0xcffc0000) >> 22)
        pde_ctx = (((pde_idx - 0x300 + 1) << 12)+0x3)
        pte_idx = ((va & 0x003ff000) >> 12)
        pte_ctx = ((pa & 0xfffff000) | (0x3))
        puts "va 0x#{va.to_s(16).rjust(8,'0')}, pa 0x#{pa.to_s(16).rjust(8,'0')}, pde_idx 0x#{pde_idx.to_s(16).rjust(8,'0')}, pde_ctx 0x#{pde_ctx.to_s(16).rjust(8,'0')}, pte_idx 0x#{pte_idx.to_s(16).rjust(8,'0')}, pte_ctx 0x#{pte_ctx.to_s(16).rjust(8,'0')}"
    end
    file.close
rescue => err
    puts "Exception: #{err}"
    err
end
