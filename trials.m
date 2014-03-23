pkg load communications

enc_len = 18;       # n Total message length, including parity symbols
msg_len = 10;       # k Message length, excluding parity symbols
sym_sz =   5;       # m bits/symbol

function retval = s2i(s)
    # Given a string where each characte represents an integer in
    # base 32 return a vector of integers
    # e.g. "0123abcdmnopv" -> [0 1 2 3 10 11 12 13 22 23 24 25 31]
    ints = int32(s);
    for i = 1:size(ints, 2)
        if (ints(i) >= 97) # "a" - "v"
            ints(i) = ints(i) - 87;
        elseif (ints(i) >= 48) # "0" - "9"
            ints(i) = ints(i) - 48;
        endif
    endfor
    retval = ints;
endfunction

function retval = i2s(ints)
    # Given a vector of integers return a string where each character
    # is the base-32 representation of an int
    # e.g. [0 1 2 3 10 11 12 13 22 23 24 25 31] -> "0123abcdmnopv"
    for i = 1:size(ints, 2)
        if (ints(i) >= 10) # "a" - "v"
            ints(i) = ints(i) + 87;
        elseif (ints(i) >= 0) # "0" - "9"
            ints(i) = ints(i) + 48;
        endif
    endfor
    retval = char(ints);
endfunction

expected = s2i(["gfhd9532dm" "4fbeu0mo"]);
disp("Expected"), disp(expected)

disp("Actuals")
# Valid primitive polynomials for a Galois Field of size 2^sym_sz
prim_polys = primpoly(sym_sz, "all", "nodisplay");

for prim_poly = prim_polys
    for fcr = 1:1024
        for prim_elem = 1:1024
            gen_poly = rsgenpoly(enc_len, msg_len, prim_poly,
                                 fcr, prim_elem);

            # A chirp as a Galois Field, of length msg_len
            msg = gf(s2i("gfhd9532dm"), sym_sz, prim_poly);

            # A complete chirp, with parity symbols, of length enc_len
            code = rsenc(msg, enc_len, msg_len, gen_poly);
            if (code.x == expected)
                disp([prim_poly, fcr, prim_elem]), disp(i2s(code.x))
            end
        end
    end
end
