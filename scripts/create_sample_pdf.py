#!/usr/bin/env python3
"""Create sample test PDF for KB (if real PDF not available)."""

import sys
from pathlib import Path

try:
    from reportlab.lib.pagesizes import letter  # type: ignore
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle  # type: ignore
    from reportlab.lib.units import inch  # type: ignore
    from reportlab.lib.colors import HexColor  # type: ignore
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak  # type: ignore
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False
    SimpleDocTemplate = None  # type: ignore
    letter = None  # type: ignore
    getSampleStyleSheet = None  # type: ignore
    ParagraphStyle = None  # type: ignore
    Paragraph = None  # type: ignore
    Spacer = None  # type: ignore
    inch = None  # type: ignore
    HexColor = None  # type: ignore


def create_sample_pdf(output_path: str) -> bool:
    """Create sample PlayReady KB PDF."""
    
    if not REPORTLAB_AVAILABLE:
        print("reportlab not available. Installing sample as text file instead.")
        return create_sample_text(output_path)
    
    try:
        doc = SimpleDocTemplate(output_path, pagesize=letter)  # type: ignore
        story = []
        styles = getSampleStyleSheet()  # type: ignore
        
        # Title
        title_style = ParagraphStyle(  # type: ignore
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=HexColor('#0066CC'),  # type: ignore
            spaceAfter=30,
        )
        story.append(Paragraph("PlayReady Digital Rights Management", title_style))  # type: ignore
        story.append(Spacer(1, 0.3*inch))  # type: ignore
        
        # Content
        content = [
            ("1. Overview", """
            PlayReady is Microsoft's digital rights management (DRM) technology designed to protect 
            audio, video, and other digital content. It provides comprehensive protection across multiple 
            platforms and devices, enabling content providers to securely distribute their intellectual property.
            """),
            
            ("2. Key Features", """
            - Multi-platform support: Windows, Mac, iOS, Android, Xbox, Smart TVs
            - High-quality streaming: Supports 4K and HDR content protection
            - Flexible licensing: Allows various business models (SVOD, TVOD, AVOD)
            - Device protection: Ensures secure playback on authorized devices only
            - Content tracking: Monitors where content is accessed and used
            - Compliance: Meets international DRM standards and regulations
            """),
            
            ("3. Technical Architecture", """
            PlayReady uses a robust client-server architecture:
            - PlayReady Client: Installed on user devices, enforces content protection
            - License Server: Issues licenses to authorized users
            - Content Delivery Network: Distributes encrypted content
            - Key Management: Secure key distribution and rotation
            
            The system employs AES encryption with 128-bit or 256-bit keys depending on content sensitivity.
            """),
            
            ("4. PlayReady License", """
            PlayReady licenses define usage rights:
            - Time-based: Expiration date and time limits
            - Device-based: Specific device identifiers
            - Format limits: Supported output resolutions
            - Copy protection: Prevents unauthorized copying
            - Analog output: Analog Devices Protection System (ADPS) integration
            """),
            
            ("5. Supported Formats", """
            PlayReady supports various media formats:
            - Video: MPEG-2, H.264 (AVC), H.265 (HEVC)
            - Audio: AAC, MP3, Dolby Digital, Dolby Atmos
            - Container: MP4, MKV, MPEG-DASH, HLS
            - Streaming: Progressive download, adaptive bitrate streaming
            """),
            
            ("6. Deployment Scenarios", """
            Common PlayReady implementations:
            - Streaming Services: Netflix, Disney+, Amazon Prime Video
            - Cable/Satellite: Protected broadcast streams
            - Enterprise: Protected educational and corporate content
            - Gaming: Xbox digital content protection
            - Smart TV: Built-in PlayReady support
            """),
            
            ("7. Security Considerations", """
            - Token-based authentication ensures only authorized users access licenses
            - Secure clock prevents license misuse
            - Revocation mechanisms disable compromised clients
            - Compliance rules enforce DRM protection at output
            - Hardware support for additional security on capable devices
            """),
        ]
        
        for heading, text in content:
            story.append(Paragraph(heading, styles['Heading2']))  # type: ignore
            story.append(Spacer(1, 0.2*inch))  # type: ignore
            story.append(Paragraph(text.strip(), styles['Normal']))  # type: ignore
            story.append(Spacer(1, 0.3*inch))  # type: ignore
        
        # Build PDF
        doc.build(story)
        print(f"✓ Sample PDF created: {output_path}")
        return True
    
    except Exception as err:
        print(f"✗ Error creating PDF: {err}")
        return create_sample_text(output_path)


def create_sample_text(output_path: str) -> bool:
    """Create sample text file as fallback."""
    try:
        content = """
# PlayReady Digital Rights Management Knowledge Base

## 1. Overview
PlayReady is Microsoft's digital rights management (DRM) technology designed to protect audio, video, and other digital content. It provides comprehensive protection across multiple platforms and devices, enabling content providers to securely distribute their intellectual property.

## 2. Key Features
- Multi-platform support: Windows, Mac, iOS, Android, Xbox, Smart TVs
- High-quality streaming: Supports 4K and HDR content protection
- Flexible licensing: Allows various business models (SVOD, TVOD, AVOD)
- Device protection: Ensures secure playback on authorized devices only
- Content tracking: Monitors where content is accessed and used
- Compliance: Meets international DRM standards and regulations

## 3. Technical Architecture
PlayReady uses a robust client-server architecture:
- PlayReady Client: Installed on user devices, enforces content protection
- License Server: Issues licenses to authorized users
- Content Delivery Network: Distributes encrypted content
- Key Management: Secure key distribution and rotation

The system employs AES encryption with 128-bit or 256-bit keys depending on content sensitivity.

## 4. PlayReady License
PlayReady licenses define usage rights:
- Time-based: Expiration date and time limits
- Device-based: Specific device identifiers
- Format limits: Supported output resolutions
- Copy protection: Prevents unauthorized copying
- Analog output: Analog Devices Protection System (ADPS) integration

## 5. Supported Formats
PlayReady supports various media formats:
- Video: MPEG-2, H.264 (AVC), H.265 (HEVC)
- Audio: AAC, MP3, Dolby Digital, Dolby Atmos
- Container: MP4, MKV, MPEG-DASH, HLS
- Streaming: Progressive download, adaptive bitrate streaming

## 6. Deployment Scenarios
Common PlayReady implementations:
- Streaming Services: Netflix, Disney+, Amazon Prime Video
- Cable/Satellite: Protected broadcast streams
- Enterprise: Protected educational and corporate content
- Gaming: Xbox digital content protection
- Smart TV: Built-in PlayReady support

## 7. Security Considerations
- Token-based authentication ensures only authorized users access licenses
- Secure clock prevents license misuse
- Revocation mechanisms disable compromised clients
- Compliance rules enforce DRM protection at output
- Hardware support for additional security on capable devices

## 8. Integration Points
PlayReady integrates with:
- Media Players: Windows Media Player, third-party players
- Content Management Systems: For license generation
- CDN Providers: For secure content delivery
- Device Manufacturers: Built-in PlayReady support
- Cloud Services: Azure Media Services integration

## 9. Best Practices
- Implement proper key management procedures
- Monitor license issuance and revocation
- Keep PlayReady clients updated
- Use strong authentication for license servers
- Implement compliance auditing
- Regular security assessments

## 10. Future Developments
PlayReady continues to evolve:
- Support for emerging video codecs (VP9, AV1)
- Enhanced streaming protection
- Improved interoperability
- Advanced usage analytics
- Zero-knowledge privacy implementations
"""
        
        # Convert to PDF if possible, else save as text with .pdf extension that can be read as text
        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        
        # Try to create actual PDF-like file, otherwise just save text
        with open(output_path.replace('.pdf', '.txt'), 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✓ Sample knowledge base created: {output_path.replace('.pdf', '.txt')}")
        print("  Note: Text file created. For PDF, install: pip install reportlab")
        return True
    
    except Exception as err:
        print(f"✗ Error creating sample content: {err}")
        return False


def main() -> int:
    """Main entry point."""
    base_path = Path(__file__).parent.parent
    pdf_path = str(base_path / "data" / "raw" / "playready_kb.pdf")
    
    print("Creating sample PlayReady KB...")
    
    if create_sample_pdf(pdf_path):
        print("\n✓ Sample KB ready for evaluation!")
        return 0
    else:
        print("\n✗ Failed to create sample KB")
        return 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
