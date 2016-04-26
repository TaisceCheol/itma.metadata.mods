<xsl:stylesheet version="1.0" 
	xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
	xmlns="http://www.loc.gov/mods/v3">
	<xsl:output method="xml" indent="yes"/>

	<xsl:template match="recordlist">
		<modsCollection xmlns:xlink="http://www.w3.org/1999/xlink"
			xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
			xmlns="http://www.loc.gov/mods/v3"
			xsi:schemaLocation="http://www.loc.gov/mods/v3 http://www.loc.gov/standards/mods/v3/mods-3-3.xsd">
			<xsl:apply-templates select="record"/>
		</modsCollection>
	</xsl:template>

	<xsl:template match="record">
		<mods>
			<xsl:apply-templates select="Title"/>
			<xsl:apply-templates select="People"/>
			<xsl:apply-templates select="DocType"/>
			<xsl:call-template name="CreationInfo"/>
			<xsl:call-template name="PublicationInfo"/>
			<xsl:apply-templates select="PhysicalDescription"/>
			<xsl:apply-templates select="Context"/>			
			<xsl:call-template  name="TableOfContents"/>
			<xsl:apply-templates select="Subjects"/>
			<xsl:apply-templates select="GeographicalLocation"/>	
			<xsl:apply-templates select="ITMAReference"/>
			<xsl:apply-templates select="InternalLink"/>
			<xsl:apply-templates select="ArchiveLocation"/>
			<xsl:apply-templates select="Copyright"/>
			<note type="statement of responsibility"><xsl:value-of select="substring-after(Title,'/ ')"/></note>
		</mods>
	</xsl:template>

	<xsl:template match="Title">
		<xsl:variable name="titleProper" select="substring-before(., ' /')"/>
		<titleInfo>
			<xsl:choose>
				<xsl:when test="$titleProper != ''">
					<title><xsl:value-of select="$titleProper"/></title>
				</xsl:when>
				<xsl:otherwise><title><xsl:value-of select="."/></title></xsl:otherwise>
			</xsl:choose>
		</titleInfo>
	</xsl:template>
	
	<xsl:template match="People">
		<name type="personal">
			<namePart type="given"><xsl:value-of select="substring-before(.,' ')"/></namePart>
			<namePart type="family"><xsl:value-of select="substring-after(.,' ')"/></namePart>
		</name>
	</xsl:template>

	<xsl:template match="DocType">
		<xsl:if test=". = 'Image'">
			<typeOfResource>still image</typeOfResource>
		</xsl:if>
		<xsl:if test=". = 'Printed Material'">
			<typeOfResource>text</typeOfResource>
		</xsl:if>
		<xsl:if test=". = 'Sound Recording'">
			<typeOfResource>sound recording</typeOfResource>
		</xsl:if>	
		<xsl:if test=". = 'Video'">
			<typeOfResource>moving image</typeOfResource>
		</xsl:if>			
	</xsl:template>

	<xsl:template match="Context">
		<abstract><xsl:value-of select="."/></abstract>
	</xsl:template>

	<xsl:template match="GeographicalLocation">
		<subject>
			<geographic><xsl:value-of select="."></xsl:value-of></geographic>
		</subject>
	</xsl:template>
	
	<xsl:template match="InternalLink">
		<location>
			<url access="raw object"><xsl:value-of select="."/></url>
		</location>
	</xsl:template>

	<xsl:template match="InternalLink">
		<location>
			<url access="raw object"><xsl:value-of select="."/></url>
		</location>
	</xsl:template>
	
	<xsl:template match="ArchiveLocation">
		<location>
			<physicalLocation>Irish Traditional Music Archive</physicalLocation>
			<holdingSimple>
				<xsl:choose>
					<xsl:when test="substring-before(.,' -- ')">
						<shelfLocator><xsl:value-of select="substring-before(.,' -- ')"/></shelfLocator>
						<shelfLocator><xsl:value-of select="substring-after(.,' -- ')"/></shelfLocator>
					</xsl:when>
					<xsl:otherwise>
						<shelfLocator><xsl:value-of select="."/></shelfLocator>
					</xsl:otherwise>
				</xsl:choose>
			</holdingSimple>
		</location>
	</xsl:template>	
	
	<xsl:template match="PhysicalDescription">
		<physicalDescription>
			<extent><xsl:value-of select="."/></extent>
		</physicalDescription>
	</xsl:template>

	<xsl:template name="PublicationInfo">
		<xsl:if test="PublisherLocation or Publisher or PublicationDate">
			<originInfo eventType="publication">
				<xsl:if test="PublisherLocation">
					<place>
						<placeTerm type="text"><xsl:value-of select="PublisherLocation"/></placeTerm>
					</place>
				</xsl:if>
				<xsl:if test="Publisher">
					<publisher><xsl:value-of select="Publisher"/></publisher>
				</xsl:if>
				<xsl:if test="PublicationDate">
					<dateIssued><xsl:value-of select="PublicationDate/@start_year"/></dateIssued>
				</xsl:if>
			</originInfo>
		</xsl:if>
	</xsl:template>

	<xsl:template name="CreationInfo">
		<xsl:if test="CreationLocation or CreationDate">
			<originInfo eventType="creation">
				<xsl:if test="CreationLocation">
					<place>
						<placeTerm type="text"><xsl:value-of select="CreationLocation"/></placeTerm>
					</place>
				</xsl:if>
				<xsl:if test="CreationDate">
					<dateIssued><xsl:value-of select="CreationDate"/></dateIssued>
				</xsl:if>
			</originInfo>
		</xsl:if>
	</xsl:template>

	<xsl:template match="Copyright">
		<accessCondition type="use and reproduction">
			<xsl:value-of select="."/>
		</accessCondition>
	</xsl:template>
	
	<xsl:template name="TableOfContents">
		<xsl:variable name="contents_concat"><xsl:apply-templates select="Contents"/></xsl:variable>
		
		<xsl:if test="$contents_concat != ''">
			<tableOfContents>
				<xsl:value-of select="$contents_concat"/>
			</tableOfContents>
		</xsl:if>
	</xsl:template>
	
	<xsl:template match="Contents">
		<xsl:if test="preceding-sibling::Contents">
			<xsl:text> -- </xsl:text>
		</xsl:if>
		<xsl:value-of select="."/>
	</xsl:template>
	
	<xsl:template match="Subjects">
			<xsl:choose>
				<xsl:when test="substring-before(.,':')">
					<subject>
						<geographic><xsl:value-of select="substring-before(.,':')"/></geographic>
						<topic><xsl:value-of select="substring-after(.,': ')"/></topic>
					</subject>
				</xsl:when>	
				<xsl:otherwise>
					<xsl:if test=". != ../GeographicLocation">
						<subject>
							<topic><xsl:value-of select='.'/></topic>
						</subject>			
					</xsl:if>
				</xsl:otherwise>
			</xsl:choose>
	</xsl:template>
	
	<xsl:template match="ITMAReference">
		<identifier type="local">
			<xsl:value-of select="."/>
		</identifier>
	</xsl:template>
	
</xsl:stylesheet>
