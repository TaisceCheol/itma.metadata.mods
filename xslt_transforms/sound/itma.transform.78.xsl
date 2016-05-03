<xsl:stylesheet version="1.0" 
	xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
	xmlns:mods="http://www.loc.gov/mods/v3">
	<xsl:output method="xml" indent="yes"/>

	<xsl:template match="recordlist">
		<mods:modsCollection xmlns:xlink="http://www.w3.org/1999/xlink"
			xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
			xmlns="http://www.loc.gov/mods/v3"
			xsi:schemaLocation="http://www.loc.gov/mods/v3 http://www.loc.gov/standards/mods/v3/mods-3-3.xsd">
			<xsl:apply-templates select="record"/>
		</mods:modsCollection>
	</xsl:template>

	<xsl:template match="record">
		<mods:mods>
			<!--	<mods:titleInfo/>	-->
			<xsl:apply-templates select="Title"/>
			
			<!--	<mods:name/>	-->
			<xsl:apply-templates select="People"/>
			
			<!--	<mods:typeOfResource/>	-->
			<xsl:apply-templates select="DocType"/>
			
			<!--	<mods:genre/>	-->
			<xsl:call-template name="Genre"/>
			
			<!--	<mods:originInfo/>	-->
			<xsl:call-template name="CreationInfo"/>
			<xsl:call-template name="PublicationInfo"/>
			
			<!--	<mods:language/>	-->
			<xsl:call-template name="Language"/>
			
			<!--	<mods:physicalDescription/>	-->
			<xsl:apply-templates select="PhysicalDescription"/>
			
			<!--	<mods:abstract/>	-->
			<xsl:apply-templates select="Context"/>
			
			<!--	<mods:tableOfContents/>	-->			
			<xsl:call-template  name="TableOfContents"/>
			
			<!--	<mods:note/>	-->
			<mods:note type="statement of responsibility"><xsl:value-of select="substring-after(Title,'/ ')"/></mods:note>
			<xsl:if test="Notes">
				<mods:note><xsl:value-of select="Notes"/></mods:note>
			</xsl:if>	
			<xsl:call-template name="Price"/>
			
			<!--	<mods:subject/>	-->			
			<xsl:apply-templates select="Subjects"/>
			<xsl:apply-templates select="GeographicalLocation"/>
			
			<!--	<mods:relatedItem/>	-->			
			<xsl:call-template name="getRelatedItems"/>
			
			<!--	<mods:identifier/>	-->			
			<xsl:apply-templates select="ITMAReference"/>	
			<xsl:apply-templates select="CatalogueNumber"/>				
			<xsl:apply-templates select="InternalLink"/>
			
			<!--	<mods:location/>	-->
			<xsl:apply-templates select="ArchiveLocation"/>	
			<xsl:apply-templates select="AlsoHeldAt"/>
			
			<!--	<mods:accessCondition/>	-->
			<xsl:call-template name="Copyright"/>
			
			<!--	<mods:recordInfo/>	-->
			<xsl:call-template name="recordInfo"/>
		</mods:mods>
	</xsl:template>

	<xsl:template match="Title">
		<xsl:variable name="titleProper" select="substring-before(., ' /')"/>
		<mods:titleInfo>
			<xsl:choose>
				<xsl:when test="$titleProper != ''">
					<mods:title><xsl:value-of select="$titleProper"/></mods:title>
				</xsl:when>
				<xsl:otherwise><title><xsl:value-of select="."/></title></xsl:otherwise>
			</xsl:choose>
		</mods:titleInfo>
	</xsl:template>
	
	<xsl:template match="People">
		<mods:name type="personal">
			<mods:namePart type="given"><xsl:value-of select="substring-before(.,' ')"/></mods:namePart>
			<mods:namePart type="family"><xsl:value-of select="substring-after(.,' ')"/></mods:namePart>
		</mods:name>
	</xsl:template>

	<xsl:template name="Genre">
		<mods:genre authority="aat" type="Concept" displayLabel="Format" authorityURI="http://vocab.getty.edu/aat/" valueURI="http://vocab.getty.edu/aat/300265790">78 rpm records</mods:genre>
	</xsl:template>

	<xsl:template match="DocType">
		<xsl:if test=". = 'Image'">
			<mods:typeOfResource>still image</mods:typeOfResource>
		</xsl:if>
		<xsl:if test=". = 'Printed Material'">
			<mods:typeOfResource>text</mods:typeOfResource>
		</xsl:if>
		<xsl:if test=". = 'Sound Recording'">
			<mods:typeOfResource>sound recording</mods:typeOfResource>
		</xsl:if>	
		<xsl:if test=". = 'Video'">
			<mods:typeOfResource>moving image</mods:typeOfResource>
		</xsl:if>			
	</xsl:template>

	<xsl:template match="Context">
		<mods:abstract><xsl:value-of select="."/></mods:abstract>
	</xsl:template>

	<xsl:template match="GeographicalLocation">
		<mods:subject>
			<mods:geographic><xsl:value-of select="."></xsl:value-of></mods:geographic>
		</mods:subject>
	</xsl:template>
	
	<xsl:template match="InternalLink">
		<mods:location>
			<mods:url access="raw object"><xsl:value-of select="."/></mods:url>
		</mods:location>
	</xsl:template>

	<xsl:template match="ArchiveLocation">
		<mods:location>
			<mods:physicalLocation>Irish Traditional Music Archive</mods:physicalLocation>
			<mods:holdingSimple>
				<xsl:choose>
					<xsl:when test="substring-before(.,' -- ')">
						<mods:shelfLocator><xsl:value-of select="substring-before(.,' -- ')"/></mods:shelfLocator>
						<mods:shelfLocator><xsl:value-of select="substring-after(.,' -- ')"/></mods:shelfLocator>
					</xsl:when>
					<xsl:otherwise>
						<mods:shelfLocator><xsl:value-of select="."/></mods:shelfLocator>
					</xsl:otherwise>
				</xsl:choose>
			</mods:holdingSimple>
		</mods:location>
	</xsl:template>	
	
	<xsl:template match="PhysicalDescription">
		<mods:physicalDescription>
			<mods:extent><xsl:value-of select="."/></mods:extent>
		</mods:physicalDescription>
	</xsl:template>

	<xsl:template match="Publisher">
		<xsl:if test="preceding-sibling::Publisher">
			<xsl:text> </xsl:text>
		</xsl:if>
		<xsl:value-of select="."/>
	</xsl:template>

	<xsl:template name="PublicationInfo">
		<xsl:variable name="publisher_info"><xsl:apply-templates select="Publisher"/></xsl:variable>
		
		<xsl:if test="PublisherLocation or Publisher or PublicationDate">
			<mods:originInfo eventType="publication">
				<xsl:if test="PublisherLocation">
					<mods:place>
						<mods:placeTerm type="text"><xsl:value-of select="PublisherLocation"/></mods:placeTerm>
					</mods:place>
				</xsl:if>
				<xsl:if test="Publisher">
					<mods:publisher><xsl:value-of select="$publisher_info"/></mods:publisher>
				</xsl:if>
				<xsl:if test="PublicationDate">
					<mods:dateIssued><xsl:value-of select="PublicationDate/@start_year"/></mods:dateIssued>
				</xsl:if>
			</mods:originInfo>
		</xsl:if>
	</xsl:template>

	<xsl:template name="CreationInfo">
		<xsl:if test="CreationLocation or CreationDate">
			<mods:originInfo eventType="creation">
				<xsl:if test="CreationLocation">
					<mods:place>
						<mods:placeTerm type="text"><xsl:value-of select="CreationLocation"/></mods:placeTerm>
					</mods:place>
				</xsl:if>
				<xsl:if test="CreationDate">
					<mods:dateIssued><xsl:value-of select="CreationDate"/></mods:dateIssued>
				</xsl:if>
			</mods:originInfo>
		</xsl:if>
	</xsl:template>

	<xsl:template name="Language">
		<mods:language>
			<xsl:for-each select="Language">
				<mods:languageTerm	type="text"><xsl:value-of select="."/></mods:languageTerm>
			</xsl:for-each>
		</mods:language>
	</xsl:template>

	<xsl:template name="Copyright">
		<mods:accessCondition type="use and reproduction" xlinkhref="http://creativecommons.org/publicdomain/mark/1.0/">This work is free of known copyright restrictions.</mods:accessCondition>
	</xsl:template>
	
	<xsl:template match="MatrixNumber">
		<mods:identifier type="matrix number">
			<xsl:value-of select="."></xsl:value-of>
		</mods:identifier>
	</xsl:template>
	
	<xsl:template name="TableOfContents">
		<xsl:variable name="contents_concat"><xsl:apply-templates select="Contents"/></xsl:variable>
		
		<xsl:if test="$contents_concat != ''">
			<mods:tableOfContents>
				<xsl:value-of select="$contents_concat"/>
			</mods:tableOfContents>
		</xsl:if>
	</xsl:template>
	
	<xsl:template match="Contents">
		<xsl:if test="preceding-sibling::Contents">
			<xsl:text> -- </xsl:text>
		</xsl:if>
		<xsl:value-of select="."/>
	</xsl:template>
	
	<xsl:template name="getRelatedItems">		
		<xsl:variable name="track_a"><xsl:value-of select="TrackA"/></xsl:variable>
		<xsl:variable name="track_b"><xsl:value-of select="TrackB"/></xsl:variable>
		
		<xsl:variable name="titleProper_track_a" select="substring-before($track_a, ' /')"/>
		<xsl:variable name="names_track_a" select="substring-after($track_a, '/ ')"/>

		<xsl:variable name="titleProper_track_b" select="substring-before($track_b, ' /')"/>
		<xsl:variable name="names_track_b" select="substring-after($track_b, '/ ')"/>
		
		<mods:relatedItem type="constituent" ID="DMD_disc01_sd001">
			<mods:titleInfo>
				<xsl:choose>
					<xsl:when test="$titleProper_track_a != ''">
						<mods:title><xsl:value-of select="$titleProper_track_a"/></mods:title>
					</xsl:when>
					<xsl:otherwise><mods:title><xsl:value-of select="$track_a"/></mods:title></xsl:otherwise>
				</xsl:choose>
			</mods:titleInfo>	
			<xsl:if test="substring-before($names_track_a, ', ')">
				<mods:name type="personal">
					<mods:namePart><xsl:value-of select="substring-before($names_track_a, ', ')"/></mods:namePart>
				</mods:name>
			</xsl:if>
			<mods:indentifier type="matrix number">
				<xsl:value-of select="(MatrixNumber)[1]"/>
			</mods:indentifier>
		</mods:relatedItem>
		
		<mods:relatedItem type="constituent" ID="DMD_disc01_sd002">
			<mods:titleInfo>
				<xsl:choose>
					<xsl:when test="$titleProper_track_b != ''">
						<mods:title><xsl:value-of select="$titleProper_track_b"/></mods:title>
					</xsl:when>
					<xsl:otherwise><mods:title><xsl:value-of select="$track_b"/></mods:title></xsl:otherwise>
				</xsl:choose>
			</mods:titleInfo>	
			<xsl:if test="substring-before($names_track_b, ', ')">
				<mods:name type="personal">
					<mods:namePart><xsl:value-of select="substring-before($names_track_b, ', ')"/></mods:namePart>
				</mods:name>
			</xsl:if>
			<mods:indentifier type="matrix number">
				<xsl:value-of select="(MatrixNumber)[2]"/>
			</mods:indentifier>
		</mods:relatedItem>		
		
		<xsl:if test="ReIssue">
			<mods:relatedItem type="otherFormat">
				<mods:note type="reissue"><xsl:value-of select="ReIssue"/></mods:note>
			</mods:relatedItem>
		</xsl:if>

		<xsl:if test="PreIssue">
			<mods:relatedItem type="otherFormat">
				<mods:note type="preissue"><xsl:value-of select="PreIssue"/></mods:note>
			</mods:relatedItem>
		</xsl:if>

	</xsl:template>
	
	<xsl:template match="Subjects">
			<xsl:choose>
				<xsl:when test="substring-before(.,':')">
					<mods:subject>
						<mods:geographic><xsl:value-of select="substring-before(.,':')"/></mods:geographic>
						<mods:topic><xsl:value-of select="substring-after(.,': ')"/></mods:topic>
					</mods:subject>
				</xsl:when>	
				<xsl:otherwise>
					<xsl:if test=". != ../GeographicLocation">
						<mods:subject>
							<mods:topic><xsl:value-of select='.'/></mods:topic>
						</mods:subject>			
					</xsl:if>
				</xsl:otherwise>
			</xsl:choose>
	</xsl:template>
	
	<xsl:template match="ITMAReference">
		<mods:identifier type="local">
			<xsl:value-of select="."/>
		</mods:identifier>
	</xsl:template>

	<xsl:template match="CatalogueNumber">
		<mods:identifier type="music publisher">
			<xsl:value-of select="."/>
		</mods:identifier>
	</xsl:template>

	<xsl:template name="recordInfo">
		<mods:recordInfo>
			<xsl:choose>
				<xsl:when test="InformationSource">
					<mods:recordContentSource><xsl:value-of select="InformationSource"/></mods:recordContentSource>
				</xsl:when>
				<xsl:otherwise>
					<mods:recordContentSource>Irish Traditional Music Archive</mods:recordContentSource>
				</xsl:otherwise>
			</xsl:choose>
			<xsl:if test="CataloguedBy">
				<mods:recordContentSource><xsl:value-of select="CataloguedBy"/></mods:recordContentSource>
			</xsl:if>
			<mods:recordOrigin>human prepared</mods:recordOrigin>
			<mods:descriptionStandard type="marcdescription">aacr</mods:descriptionStandard>		
		</mods:recordInfo>
	</xsl:template>

	<xsl:template name="Price">
		<xsl:if test="Price">
			<mods:note type="price"><xsl:value-of select="Price"/></mods:note>
		</xsl:if>
	</xsl:template>
	
	<xsl:template match="AlsoHeldAt">
		<mods:location>
			<mods:holdingSimple>
				<mods:copyInformation>
					<mods:note type="also held at"><xsl:value-of select="."/></mods:note>
				</mods:copyInformation>	
			</mods:holdingSimple>
		</mods:location>
	</xsl:template>
</xsl:stylesheet>
