# -*- mode: python -*-
a = Analysis(['PDF-merger-for-DS.py'],
             pathex=['D:\\Programs-Archive\\PDF-merger-for-DS-python\\PyInstaller-2.1\\PDF-merger-for-DS'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='PDF-merger-for-DS.exe',
          debug=False,
          strip=None,
          upx=True,
          console=True )
