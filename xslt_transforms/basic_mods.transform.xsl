<xsl:stylesheet version="1.0" 
	xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
	xmlns:mods="http://www.loc.gov/mods/v3"
	xmlns:exsl="http://exslt.org/common" 
	exclude-result-prefixes="exsl">
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
			<xsl:apply-templates select="AlternativeTitle"/>
			<xsl:call-template name="generateAltTitles"/>
			
			<!--	<mods:name/>	-->
			<xsl:apply-templates select="People"/>
			<xsl:apply-templates select="People/@name"/>
			
			<!--	<mods:typeOfResource/>	-->
			<xsl:apply-templates select="DocType"/>
			
			<!--	<mods:genre/>	-->
			<xsl:call-template name="Genre"/>
			
			<!--	<mods:originInfo/>	-->
			
			<!--	<mods:language/>	-->
			<xsl:call-template name="Language"/>
			
			<!--	<mods:physicalDescription/>	-->
			<xsl:apply-templates select="PhysicalDescription"/>
			
			<!--	<mods:subject/>	-->			
			<xsl:apply-templates select="Subjects"/>
			<xsl:apply-templates select="GeographicalLocation"/>
			
			<!--	<mods:identifier/>	-->			
			<xsl:apply-templates select="ITMAReference"/>	
			<mods:identifier type="local">CID-<xsl:value-of select="@CID"/></mods:identifier>
		</mods:mods>
	</xsl:template>

	<xsl:template match="Title">
		<xsl:variable name="titleProper" select="substring-before(.,'/')"/>
		<mods:titleInfo>
			<xsl:choose>
				<xsl:when test="$titleProper != ''">
					<mods:title><xsl:value-of select="normalize-space($titleProper)"/></mods:title>
				</xsl:when>
				<xsl:otherwise><mods:title><xsl:value-of select="."/></mods:title></xsl:otherwise>
			</xsl:choose>
		</mods:titleInfo>
	</xsl:template>
	
	<xsl:template match="AlternativeTitle">
		<xsl:variable name="titleProper" select="substring-before(.,'/')"/>
		<mods:titleInfo type="alternative">
			<xsl:choose>
				<xsl:when test="$titleProper != ''">
					<mods:title><xsl:value-of select="normalize-space($titleProper)"/></mods:title>
				</xsl:when>
				<xsl:otherwise><mods:title><xsl:value-of select="."/></mods:title></xsl:otherwise>
			</xsl:choose>
		</mods:titleInfo>
	</xsl:template>	
	
	<xsl:template name="generateAltTitles">
		<xsl:variable name="titleProper" select="substring-before(Title,'/')"/>
		<xsl:if test="substring-before($titleProper,'=')">
			<mods:titleInfo type="alternative">
				<mods:title><xsl:value-of select="normalize-space(substring-before($titleProper,'='))"/></mods:title>
			</mods:titleInfo>
			<mods:titleInfo type="alternative">
				<mods:title><xsl:value-of select="normalize-space(substring-after($titleProper,'='))"/></mods:title>
			</mods:titleInfo>			
		</xsl:if>
	</xsl:template>
	
	<xsl:template match="People">
		<mods:name type="personal">
			<mods:namePart type="given"><xsl:value-of select="substring-before(.,' ')"/></mods:namePart>
			<mods:namePart type="family"><xsl:value-of select="substring-after(.,' ')"/></mods:namePart>
		</mods:name>
	</xsl:template>

	<xsl:template match="People/@name">
		<mods:name type="personal">
			<mods:namePart type="given"><xsl:value-of select="substring-before(.,' ')"/></mods:namePart>
			<mods:namePart type="family"><xsl:value-of select="substring-after(.,' ')"/></mods:namePart>
			<xsl:if test="../Role">
				<mods:role>
					<mods:roleTerm type="code" authorityURI="{../Role/@authorityURI}" valueURI="{../Role/@valueURI}">
						<xsl:value-of select="../Role/@code"/>	
					</mods:roleTerm>	
					<mods:roleTerm type="text" authorityURI="{../Role/@authorityURI}" valueURI="{../Role/@valueURI}">
						<xsl:value-of select="../Role"/>	
					</mods:roleTerm>	
				</mods:role>	
			</xsl:if>	
		</mods:name>
	</xsl:template>

	<xsl:template name="Genre">
		<mods:genre authority="aat" type="Concept" displayLabel="Format" authorityURI="http://vocab.getty.edu/aat/" valueURI="http://vocab.getty.edu/aat/300028051">books</mods:genre>		
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
			<xsl:if test="following-sibling::RunningTime">
				<mods:note type="running-time"><xsl:value-of select="following-sibling::RunningTime"/></mods:note>
			</xsl:if>
		</mods:physicalDescription>
	</xsl:template>
	<xsl:template name="Language">
		<xsl:if test="Language">
			<mods:language>
				<xsl:for-each select="Language">
					<mods:languageTerm	type="text"><xsl:value-of select="."/></mods:languageTerm>
				</xsl:for-each>
			</mods:language>
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

	<xsl:template name="tokenize">
		<xsl:param name="pText" select="."/>
		<xsl:variable name="delimiter" select="'&lt;br&gt;'"/>		
		<xsl:if test="string-length($pText) >0">
			<mods:titleInfo>
				<mods:title>
					<xsl:value-of select="substring-before(concat($pText, $delimiter), $delimiter)"/>
				</mods:title>
			</mods:titleInfo>
			<xsl:call-template name="tokenize">
				<xsl:with-param name="pText" select=
					"substring-after($pText, $delimiter)"/>
			</xsl:call-template>
		</xsl:if>
	</xsl:template>	
	
</xsl:stylesheet>
