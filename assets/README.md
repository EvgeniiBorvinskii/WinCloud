# WinCloud Logo Placeholder

Place your logo images here:
- wincloud.png (main logo, 512x512px recommended)
- wincloud2.png (alternative logo)
- wincloud.ico (icon for Windows executable)

## Design Guidelines

### Main Logo (wincloud.png)
- Size: 512x512px (PNG with transparency)
- Style: Modern, clean, professional
- Colors: Blue/white theme recommended
- Should represent cloud + archiving concept

### Alternative Logo (wincloud2.png)
- Size: 256x256px or larger
- Can be more detailed or have text
- Used in splash screens, about dialog

### Icon (wincloud.ico)
- Windows .ico format
- Multiple sizes: 16x16, 32x32, 48x48, 256x256
- Should be recognizable at small sizes
- Used for application icon and file type association

## Creating Icons

You can use online tools to convert PNG to ICO:
- https://icoconvert.com/
- https://convertio.co/png-ico/

Or use ImageMagick:
```bash
magick convert wincloud.png -define icon:auto-resize=256,128,64,48,32,16 wincloud.ico
```

## File Association

When users install WinCloud, .cloud files will use wincloud.ico as their icon.
