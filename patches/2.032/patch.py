#!/usr/bin/env python2
# Promiscuous Mode Patch for MD380 Firmware
# Applies to version 2.032

from Patcher import Patcher

if __name__ == '__main__':
    print "Creating patches from unwrapped.img.";
    patcher=Patcher("unwrapped.img");
    
    #Old logo patcher, no longer used.
    #fhello=open("welcome.txt","rb");
    #hello=fhello.read();
    #patcher.str2sprite(0x08094610,hello);
    #print patcher.sprite2str(0x08094610,0x14,760);
    
    #Old patch, matching on the first talkgroup.
    #We don't use this anymore, because the new patch is better.
    #patcher.nopout(0x0803ee36,0xd1ef);
    
    # New patch for monitoring all talk groups , matched on first
    # entry iff no other match.
    #wa mov r5, 0 @ 0x0803ee86 # So the radio thinks it matched at zero.
    patcher.sethword(0x0803ee86, 0x2500);
    #wa b 0x0803ee38 @ 0x0803ee88 # Branch back to perform that match.
    patcher.sethword(0x0803ee88,0xe7d6); #Jump back to matched condition.
    #patcher.export("prom-public.img");
    
#     #These aren't quite enough to skip the Color Code check.  Not sure why.
#     patcher.nopout(0x0803ea62,0xf040);  #Main CC check.
#     patcher.nopout(0x0803ea64,0x80fd);
#     patcher.nopout(0x0803e994,0xf040);  #Late Entry CC check.
#     patcher.nopout(0x0803e996,0x8164);
#     patcher.sethword(0x0803fd8e,0xe02d, #Check in dmr_dll_parser().
#                      0xd02d);
#     patcher.nopout(0x0803eafe,0xf100); #Disable CRC check, in case CC is included.
#     patcher.nopout(0x0803eb00,0x80af);
    
    
    #patcher.export("prom-colors.img");
    
    
    # This should be changed to only show missed calls for private
    # calls directed at the user, and to decode others without
    # triggering a missed call.
    patcher.nopout(0x0803ef10,0xd11f);  #Matches all private calls.
    #patcher.export("prom-private.img");
    
    

    #Everything after here is experimental.
    #Everything after here is experimental.
    #Everything after here is experimental.
    
    #This cuts out the Chinese font, freeing ~200k for code patches.
    patcher.ffrange(0x809c714,0x80d0f80);
    
    #This mirrors the RESET vector to 0x080C020, for use in booting.
    patcher.setword(0x0800C020,
                    patcher.getword(0x0800C004),
                    0x00000000);


    #This makes RESET point to our stub below.
    patcher.setword(0x0800C004,
                    0x0809cf00+1
    );
    
    
    #This stub calls the target RESET vector,
    #if it's not FFFFFFFF.
    patcher.sethword(0x0809cf00, 0x4840);
    patcher.sethword(0x0809cf02, 0x2100);
    patcher.sethword(0x0809cf04, 0x3901);
    patcher.sethword(0x0809cf06, 0x4508);
    patcher.sethword(0x0809cf08, 0xd100);
    patcher.sethword(0x0809cf0a, 0x483c);
    patcher.sethword(0x0809cf0c, 0x4700);
    # [0x0809cf00]> pd 7
    #             0x0809cf00      4048           ldr r0, [pc, 0x100]         ; [0x809d004:4]=-1
    #             0x0809cf02      0021           movs r1, 0
    #             0x0809cf04      0139           subs r1, 1
    #             0x0809cf06      0845           cmp r0, r1
    #         ,=< 0x0809cf08      00d1           bne 0x809cf0c
    #         |   0x0809cf0a      3c48           ldr r0, [pc, 0xf0]          ; [0x809cffc:4]=0x80fa969 
    #         `-> 0x0809cf0c      0047           bx r0
    # [0x0809cf00]> 

    
    #Stores the RESET handler for our stub.
    patcher.setword(0x809cffc,
                    patcher.getword(0x0800C020),
                    0xFFFFFFFF);
    
    
    #Marks the version as "md380tools"
    patcher.setwstring(0x080d14d8,
                      "MD380Tools Ver.");
    
    #Change the manufacturer string.
    patcher.setstring(0x080f9e4c,
                      "Travis Goodspeed KK4VCZ");
    #Change the device name.
    patcher.setstring(0x080d1820,
                      "Patched MD380");
    
    #Fixes a typo in 2.032.  Unneeded in 2.034.
    patcher.setwstring(0x080d17e8,
                      "Repeater Slot"); #was 'Repeatar Slot'
    
    patcher.export("experiment.img");
    
