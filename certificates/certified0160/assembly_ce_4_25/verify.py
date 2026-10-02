#!/usr/bin/python3
"""Confined record delivery with unchanged bank786 mathematics, accepted795
composition audit, and COMPLETE LIVE independently authored recovery proof.
No pending bank fact or ready flag is a proof input. See RELEASE_PROOF.md.
"""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib,subprocess,sys
from release_gate import current_cut,record_arithmetic,load,constructive_cut
PINS={'ASSEMBLY.md': '2b3dfe94fa9ca4a541f824abac045f581ad52a885f34608d07b87664489745e1', 'AUDIT_EDGES.json': 'c4a766a96ab022c35f8cfc6a92c373e3d3e21e0e24fca4bdd522741af38a3581', 'BANK_SNAPSHOT.json': '97d23c881c4d961b03bab45be78ae2c76c6e6fee6f9f641593780122c4b322c7', 'CALIBRATIONS.json': '45063d29018d8fcc7fb1c083af53b2adbb2195cc344dca13d6f23ebfda1e679d', 'LIVE_RECOVERY_ARITHMETIC.md': '9d70bc4608b6af215c5bc56629ba88b48a06ca3c4fde9808b236dcca553348be', 'LIVE_RECOVERY_PROOF.md': '8fea6e09a1a4001811e94bb4a467abe1cc8af1f81ae02fbb0983a0ec561c8ddc', 'ORIGINS.json': '456faf51605c19acac3c106ee99eeb28878529400058052287b7765eaea1ada2', 'PREREG.md': '0e908ed6de418c2c4ff507c0d0999a3432e7b8ff014f8485ad8b18be5ec5df53', 'QUALIFICATION_BINDINGS.json': '81c2d6d807adc28e333f07fd49ebc4de7a5112f0087b44afd4bd9b150388d2d8', 'RECOVERY_LIVE.json': 'a4c29b98a06a07d0e896a1e4293fa47eac5a6bf5f4a32280532a8e0063d3329b', 'RELEASE_CONTRACT.json': '84c94390a545b43463de35e45102f25018fb53de0f4c82c426c22ad032f6e138', 'RELEASE_PROOF.md': 'e2c0b8e7dc8e459b36e3ed1cc55c6ed76f890b8c313ab99e01b5f5ebbf8f64f0', 'REPLAY_CONTRACT.json': '41648a4d19257f50ce7502e6a3340e719b7ea7f43ce22eed3870722e56569264', 'frozen/ACCEPTED_SOURCE_TEXTS.json': 'd5004326debc05a90e5a813ecb6f766f0d1f51fb46b55a4345c1e805f0c50799', 'frozen/accepted786_stdout.txt': 'e55cfc52690c2177ee2ec865dd8f2530ec71f2daa3e11e05012646c995bd95aa', 'frozen/external789_AUDIT.txt': '3da4fcfd073884f7e8c25919ecbaade9cac7c4ae07437185c0ed7dc22fed5684', 'frozen/external789_COMPLETE_RESULTS.json': '58db76fc8a5597fc4097996cee3cc14bf54578c95b5d48588fc70ecbff5e73d8', 'frozen/external789_LEAF_RESULTS.json': '3d46cd814c4e3aa5f0d9514555cbf3f89e43468b19a94d87cfb10808b8ab3cbd', 'frozen/external789_ORIGINAL_PRODUCT_DIGESTS.json': 'e82910cd33531b01ef59d083e0d2795990f90262ded159f9ab07c7eef99fb4d7', 'frozen/external789_SUMMARY.json': 'ec53e01772655ca1eab9bf522df996919d0b1bb4580f5a81ddd758d0d07d5d1e', 'frozen/external795_ARITHMETIC.txt': 'a19a79aec16a2beec9947a17b3004b9fc619713ed4829c629e7c0a6b031ee8ea', 'frozen/external795_AUDIT.txt': 'd286763b56d295af80c413b3a5946c989775796f7310c0cb302663a710ce14c6', 'frozen/external795_CONTROLS.json': '422612f28fa60307908ea837846be1b955dd42912885735d5f748a70a41de4b3', 'frozen/external795_LOGICAL.json': '376f80bd05526b78142b229d385a8aad7afa796cec545b9a8adc8b7a7d2f469e', 'frozen/external795_NUMERICAL.json': '7e2aa07512e70000a07f1bccd909d7c97a0aa49945093d5c1c2e174e71de9567', 'frozen/external795_SUMMARY.json': '14b0a8763bd1c7b4aef10f3183a87e423f9b04b87faedc79c3f0ceea87ce9af0', 'math/ASSEMBLY.md': 'a6c620eb9ffd110b641982129b1173bc4c7aa4262afc2f12ab08a2451f81773c', 'math/CITATIONS.json': 'ef9111d59d67d50a6efd2f1411f4d2775b00549d55e38a5dc65a3a9aef645959', 'math/CONTRACTS.json': 'fa81345dd718f697811eaba3238b59c35091a3d97c839f8baee38580e385b545', 'math/FACT.txt': '0ec8e7cd2daafe4274b8072659796837b62fe464e3e8bb9420dbc1eaff2fa273', 'math/FROZEN.sha256': 'a7193ee6cb45583d0214fc5b5a990cdda3053a022ca18f27f19d3b314359f34e', 'math/PREREG.md': '1216500da8bc30012ae632111ef7d028ce84e6f61ce4b81e06af82461cd898f4', 'math/PROVENANCE.json': 'c2e7782b8f00d072be98ccb8612d0982812ec236da2e328e97d1a38da4482554', 'math/QUANTIFIER_AUDIT.md': '722bb0eddbd53e48b6a5f415f285c41b56198c83bbeb4403c7693c7880da0397', 'math/READINESS.json': '772cfe1d67df12ba084fee1fe1781e564eccd9cc0311fd440bf1328d08cc40f0', 'math/SECOND_PROOF.md': '640dab98b73910c413749ebcb43853b96ddfbaeb0f0f62770c79e14cf2e2dcb4', 'math/SOURCES.sha256': '9412fef5dce0b7a695ff6af9c2e05e2b5bf0f458bf5f330a31023e023e37f700', 'math/frozen/analytic_separator_second.txt': 'fd5e4f351cdaf71dd2b0dfe505a48b95965be5db915403e2d3787a19e455d5df', 'math/frozen/anchor.txt': '874957ddc1caa202aeffa7573013dc161854c39b3f832d367fd5cd008e9ccb54', 'math/frozen/bank720_theorem.txt': '249aa74644189dd15c0e5bf9e6fcddcfd576e242bb2660542c844f8c0fe4bff3', 'math/frozen/bank725_audit.txt': '4ae59adc397d9e31bf1d0ca2cb4565943a2840495c7f4bfaba3534a7584fde35', 'math/frozen/bank729_primary.json': '463e204585233314aeeb78c4b0f3723907e713180c2def062f94b287634c8c56', 'math/frozen/bank729_proof.txt': '2415dac9b1ef172267133ce3f9a493621a671243295f6bf3a645c15e4c665191', 'math/frozen/bank729_second.json': 'f8685c1bfeca0a21bfd69a6390dbf4ffff482320d49e597c7bb34dc2ce3d03eb', 'math/frozen/bank733_audit.txt': 'f25f28713b887a2b26d120ad8cc7207b55ef537cf1a2a33682cf83b503f9365e', 'math/frozen/bank738_primary.json': '3fbb21ec83d23588a73fc53511a6fc177ff69be020c419ee0c82d6d0bab03d09', 'math/frozen/bank738_proof.txt': '0837a258f15c47d50f8186701d8b701129af415e1ecbd5b64572cf04fac33a92', 'math/frozen/bank744_proof.txt': '2c688d63297c8bb60ba9faa801aa2d4a40fca65a0c90f9b80b148624e8874f10', 'math/frozen/bank754_audit.txt': 'ca2b8e0d5adf4768b57b625cd26ac8070e8449446d7147f34da96cd67a3f64fa', 'math/frozen/bank754_summary.json': '319a25d21b25970d58b9aaf165c305bdb2cd82df6d99486a10673e9ee22a16d9', 'math/frozen/bank767_geometry.json': 'f9a2a6e1a4181c7a56ca457342b3e0680deda8f1aafb847cfeae3a97238caeb6', 'math/frozen/bank767_leaves_primary.txt': '3ed5ee0c88248509ed9fd2b30337e3736d09039050f5166a7a982a3e16ce73c5', 'math/frozen/bank767_leaves_second.txt': 'dec6c0a8b2ff9559a3cf90a5cf75a11c4ae79752d99e92558e186ae314fe37c5', 'math/frozen/bank767_outputs.txt': '613d7df7f03c68af80e8a933ebe521ea6ab84f7bb5268c240155d18a5832c7df', 'math/frozen/bank767_proof.txt': '026b89ecc2fe2e42ef5dc62c513c01b567da609f4f73f7a6b7f6d8528022d806', 'math/frozen/bank767_secondproof.txt': '16310586a87b2bff2be351fc421ca3b7f1f3e643f8fc8068d23fde0e72300a7d', 'math/frozen/bank767_summary.json': '092da4612e585c102d19d63e07128111dd53147b0339219489091d64ef204baa', 'math/frozen/bank772_audit.txt': '678414019adc389f3c85815bb73012b9c6d8db4cd7ab1718dcc3625f82a162e9', 'math/frozen/bank772_summary.json': 'adf0f852114db7ece61eead8ed40c89b880d73c1d026a0e638a5d25776b4ce89', 'math/frozen/bank774_bins.txt': '94d0610a407a302ee18a2330cf48ebc94cbf34c74fc20f6545de41de667f8f1e', 'math/frozen/bank774_build_primary.c': '19bc55ec0eb5634bda211f41a350982df9937e5e3d7819687d828f2001e0af23', 'math/frozen/bank774_build_second.txt': 'bd4b83859f25c88ce213f5c150241ba2636a54142e0cf217ecd0b314d1bf6ee9', 'math/frozen/bank774_geometry.json': '1d6a6dc0577e18dd4c6bb49b8b746e353f7bf40490368ea032a3c24019a497d5', 'math/frozen/bank774_outputs.txt': '3e8f4148cd6880fd7e0533074e2a40a624e4b40bf13b8d61a40a125626e377f2', 'math/frozen/bank774_primary.json': 'a83bcadbd63c5ba04be0a98ffa628d6b666616af944343de5b5a86a38e600137', 'math/frozen/bank774_probes.json': '1c2d17ecb293dfa584921bee211731f645d7c2951e706950156ffa4c88da6956', 'math/frozen/bank774_proof.txt': '41e09d60548b65e2c09c8c374c6e3a9378141fc9817998f2d527bdb8c45d44d8', 'math/frozen/bank774_second.json': '2d7227cd3797de39934feaae909d6c69cceecad457c9acafeadde115f12a0c8b', 'math/frozen/bank774_secondproof.txt': 'e567ecd65edd93cdd967e6757afba5767efd5babee6577830b3b2944d3ea27c5', 'math/frozen/bank774_source_pins.json': '6d9a1ba0a7d661fbe3625190b0fc13b18d9bec9ad47c02660f0c6d43ad6e468f', 'math/frozen/bank774_summary.json': 'e00c5a340faa03fca859c7bd7f67cfdccfebaf84a97f239c01cc5adc9e5db8e8', 'math/frozen/boundary_proof.txt': '2bebe2da8c1f28ed99ea856fe2d8134842ec450046077a8549374d84bbb56a54', 'math/frozen/hermite_separator.txt': '70cc54cfc3932efaa495687dc3565f9af090594deca67b65faa88dde853cc196', 'math/frozen/interior.txt': 'bdc313246fb5927e7605ba048deca2c2b0566eda9fb98a2a12cae8f53c9d1842', 'math/frozen/interior_audit.json': '097749381b59ae0e47bf7d38ed11fad4df9789c378333bbc47ecc8c88a9d1342', 'math/frozen/remote_tail.txt': 'b25f0abb8cccd94b36ea5ec89324c40d80f64724b8de82a40af7a885827069c9', 'math/frozen/remote_tail_second.txt': '78f6e660c543d9a1a6c741716197b60e58b05130e0b6f81490a7d0da1fe61b06', 'math/frozen/separator_second_summary.json': 'e81b4ff81fb81da5141feeed77b90d2a8193e6c669924d83a37d64b09fbb10be', 'math/second_line.py': '0674cdc709a12bcdf1c9957bcab64e9bcfe2e0d8c6ecee8c342029c47e6d1313', 'math/verify.py': '8443786a74ca72114f30e4c6ba1acea36937efe78d8e848b8331ae046e3cd20f', 'recovery_live.py': '8a92674730cba7304b0616e666899b51b45a8bffb2bc8b88591f19a00222f4b2', 'release_gate.py': '85dcf600db1710081392506a38bbe27cf5df4c1c5f9747db4610dd1c7eab5328'}


def pinned_inputs():
    got={}
    for line in Path('FROZEN.sha256').read_text().splitlines():
        if not line or line.startswith('#'):continue
        h,n=line.split();p=Path(n)
        assert not p.is_absolute() and '..' not in p.parts and n not in got
        assert hashlib.sha256(p.read_bytes()).hexdigest()==h
        got[n]=h
    assert got==PINS and got
    for line in Path('SOURCES.sha256').read_text().splitlines():
        h,n=line.split();p=Path(n)
        assert not p.is_absolute() and '..' not in p.parts
        assert hashlib.sha256(p.read_bytes()).hexdigest()==h
    return len(got)


def replay_math():
    # Same interpreter, inherited confinement and local cwd only. All accepted
    # source inputs remain byte-exact; the child calls its independent line.
    p=subprocess.run([sys.executable,'verify.py'],cwd='math',capture_output=True,text=True,timeout=150)
    Path('mathematics.log').write_text(p.stdout);Path('mathematics_stderr.log').write_text(p.stderr)
    replay=load('REPLAY_CONTRACT.json')
    assert p.returncode==0 and not p.stderr
    assert hashlib.sha256(p.stdout.encode()).hexdigest()==replay['math_stdout_sha256']
    assert p.stdout.splitlines().count('RESULT: ALL PASS')==1
    assert not any(l.startswith('RECORD_') for l in p.stdout.splitlines())
    for n,h in replay['math_outputs'].items():
        assert hashlib.sha256((Path('math')/n).read_bytes()).hexdigest()==h
    for line in p.stdout.splitlines():
        if line.startswith(('RESULT','TOTAL CHECKS RUN:','RELEASE_STATUS','MATHEMATICAL_CONCLUSION')):continue
        print(line)
    result=load('math/RESULT.json');assert result['candidate_release']=='HELD'
    assert result['snapshot']==777 and not result['new_source_production'] and not result['official_attestation']
    assert len(result['leaves'])==14 and result['exact']['entry_count']=='1609011'
    return result


def main():
    n=pinned_inputs();math=replay_math();arithmetic=record_arithmetic();accepted=current_cut()
    for k,mkey in [('lambda_upper','a'),('t_hi','b'),('X','X'),('RH_margin','RH_margin')]:
        assert F(arithmetic[k])==F(math['exact'][mkey])
    # The return value comes from an actual complete child execution during
    # this invocation, never by reading a preexisting live-summary file.
    from recovery_live import execute
    live=execute()
    cut=constructive_cut(accepted,live,load('RELEASE_CONTRACT.json'))
    assert cut['ready'] and cut['missing']==[] and not cut['live_bank_acceptance_asserted']
    output={'candidate_release':'CONSTRUCTIVE_COMPLETE','mathematical_source':786,
            'mathematics_fresh':True,'math_checks':math['checks'],'math_second_checks':math['second_checks'],
            'frozen_files':n,'arithmetic':arithmetic,'accepted_only_qualification':accepted,
            'constructive_qualification':cut,'live_recovery_checks':live['checks'],
            'live_execution_sha256':hashlib.sha256(Path('LIVE_EXECUTION.json').read_bytes()).hexdigest(),
            'record_lines_emitted':5,'new_bound_claimed_as_fact':False,'official_attestation':False,
            'candidate_accepted':False,'publication_approved':False}
    Path('RELEASE_RESULT.json').write_text(json.dumps(output,indent=2,sort_keys=True)+'\n')
    print('TARGET_SCORE FLOOR10',arithmetic['FLOOR10'],'CEIL10',arithmetic['CEIL10'])
    print('EXTERNAL_ACCEPTED memory789 targets767; memory795 targets786; neither audits774')
    print('EXTERNAL_RECOVERY_COMPLETE_LIVE functional_astra-s27; NO_UNCAPTURED_ACCEPTANCE_CITED')
    print('CONSTRUCTIVE_CUT missing_count',len(cut['missing']))
    print('RECORD_LAMBDA_UPPER =',arithmetic['lambda_upper'])
    print('RECORD_T_LO =',arithmetic['t_lo'])
    print('RECORD_T_HI =',arithmetic['t_hi'])
    print('RECORD_ANCHOR =',arithmetic['anchor_upper'])
    print('RECORD_X =',arithmetic['X'])
    print('TOTAL CHECKS RUN:',math['checks']+math['second_checks']+live['checks'])
    print('RESULT: ALL PASS')
    return 0


if __name__=='__main__':raise SystemExit(main())
